from __future__ import annotations
import asyncio
from datetime import datetime
from typing import Iterable, TYPE_CHECKING

from loguru import logger

from fazdb.api.wynn.response import GuildResponse, OnlinePlayersResponse, PlayerResponse
from fazdb.db.fazdb.model import FazdbUptime
from fazdb.util import ApiResponseAdapter

from .task import Task

if TYPE_CHECKING:
    from . import RequestQueue, ResponseQueue
    from fazdb import Api, IFazdbDatabase


class TaskDbInsert(Task):
    """ Inserts API responses to database. """

    def __init__(
        self,
        api: Api,
        db: IFazdbDatabase,
        request_queue: RequestQueue,
        response_queue: ResponseQueue,
    ) -> None:
        self._api = api
        self._db = db
        self._request_queue = request_queue
        self._response_queue = response_queue

        self._event_loop = asyncio.new_event_loop()
        self._latest_run = datetime.now()
        self._response_adapter = ApiResponseAdapter()
        self._response_handler = self._ResponseHandler(self._api, self._request_queue)
        self._start_time = datetime.now()

    def setup(self) -> None:
        self._event_loop.run_until_complete(self._db.create_all())
        # NOTE: Initial request. Results in a chain reaction of requests.
        self._request_queue.enqueue(0, self._api.player.get_online_uuids(), priority=999)

    def run(self) -> None:
        with logger.catch(level="ERROR"):
            self._event_loop.run_until_complete(self._run())
        self._latest_run = datetime.now()

    async def _run(self) -> None:
        await self._db.fazdb_uptime_repository.insert(
            FazdbUptime(start_time=self._start_time, stop_time=datetime.now()),
            replace_on_duplicate=True
        )

        online_players_resp: None | OnlinePlayersResponse = None
        player_resps: list[PlayerResponse] = []
        guild_resps: list[GuildResponse] = []
        for resp in self._response_queue.get():
            if isinstance(resp, PlayerResponse):
                player_resps.append(resp)
            elif isinstance(resp, OnlinePlayersResponse):
                online_players_resp = resp
            elif isinstance(resp, GuildResponse):
                guild_resps.append(resp)

        # NOTE: Make sure responses are handled first before inserting.
        # NOTE: Insert online players requires the most recent response_handler.online_players data.
        self._response_handler.handle_onlineplayers_response(online_players_resp)
        self._response_handler.handle_player_response(player_resps)
        self._response_handler.handle_guild_response(guild_resps)

        await self._insert_online_players_response(online_players_resp)
        await self._insert_player_responses(player_resps)
        await self._insert_guild_response(guild_resps)

    async def _insert_online_players_response(self, resp: OnlinePlayersResponse | None) -> None:
        if not resp or not resp.body.raw: return
        adapter = self._response_adapter.OnlinePlayers

        db = self._db
        async with db.enter_session() as session:
            await db.online_players_repository.truncate(session)
            await db.online_players_repository.insert(adapter.to_online_players(resp), session)
            await session.flush()

            await db.player_activity_history_repository.insert(
                adapter.to_player_activity_history(resp, self._response_handler.online_players),
                session=session,
                replace_on_duplicate=True
            )
            await session.flush()

            worlds = list(adapter.to_worlds(resp))
            await db.worlds_repository.delete([world.name for world in worlds])
            await db.worlds_repository.insert(worlds, replace_on_duplicate=True, columns_to_replace=["player_count"])
            await session.flush()

    async def _insert_player_responses(self, resps: list[PlayerResponse]) -> None:
        if not resps: return

        adapter = self._response_adapter.Player
        character_history = []
        character_info = []
        player_history = []
        player_info = []
        for resp in resps:
            character_history.extend(adapter.to_character_history(resp))
            character_info.extend(adapter.to_character_info(resp))
            player_history.append(adapter.to_player_history(resp))
            player_info.append(adapter.to_player_info(resp))

        db = self._db
        await db.player_info_repository.insert(player_info, replace_on_duplicate=True)
        await db.character_info_repository.insert(character_info, ignore_on_duplicate=True)
        await db.player_history_repository.insert(player_history, ignore_on_duplicate=True)
        await db.character_history_repository.insert(character_history, ignore_on_duplicate=True)

    async def _insert_guild_response(self, resps: list[GuildResponse]) -> None:
        if not resps: return

        adapter = self._response_adapter.Guild
        guild_info = []
        guild_history = []
        guild_member_history = []
        for resp in resps:
            guild_info.append(adapter.to_guild_info(resp))
            guild_history.append(adapter.to_guild_history(resp))
            guild_member_history.extend(adapter.to_guild_member_history(resp))

        db = self._db
        await db.guild_info_repository.insert(guild_info, ignore_on_duplicate=True)
        await db.guild_history_repository.insert(guild_history, ignore_on_duplicate=True)
        await db.guild_member_history_repository.insert(guild_member_history, ignore_on_duplicate=True)

    @property
    def response_handler(self) -> TaskDbInsert._ResponseHandler: return self._response_handler

    @property
    def first_delay(self) -> float: return 1.0

    @property
    def interval(self) -> float: return 5.0

    @property
    def latest_run(self) -> datetime: return self._latest_run

    @property
    def name(self) -> str: return self.__class__.__name__


    class _ResponseHandler:
        """ Handles Wynncraft response processing, queueing, and requeuing. """

        def __init__(self, api: Api, request_list: RequestQueue) -> None:
            self._api = api
            self._request_list = request_list

            self._online_guilds: dict[str, set[str]] = {}
            self._online_players: dict[str, datetime] = {}
            self._logged_on_guilds: set[str] = set()
            self._logged_on_players: set[str] = set()

        def handle_onlineplayers_response(self, resp: None | OnlinePlayersResponse) -> None:
            if not resp: return
            self._process_onlineplayers_response(resp)
            self._requeue_onlineplayers(resp)
            self._enqueue_player()

        def handle_player_response(self, resps: Iterable[PlayerResponse]) -> None:
            if not resps: return
            self._process_player_response(resps)
            self._requeue_player(resps)
            self._enqueue_guild()

        def handle_guild_response(self, resps: Iterable[GuildResponse]) -> None:
            if not resps: return
            self._requeue_guild(resps)

        # OnlinePlayersResponse
        def _process_onlineplayers_response(self, resp: OnlinePlayersResponse) -> None:
            new_online_uuids: set[str] = {str(uuid) for uuid in resp.body.players}
            prev_online_uuids: set[str] = set(self.online_players)

            logged_off: set[str] = prev_online_uuids - new_online_uuids
            self._logged_on_players: set[str] = new_online_uuids - prev_online_uuids

            for uuid in logged_off:
                del self.online_players[uuid]

            for uuid in self.logged_on_players:
                self.online_players[uuid] = resp.headers.to_datetime()

        def _enqueue_player(self) -> None:
            for uuid in self.logged_on_players:
                self._request_list.enqueue(0, self._api.player.get_full_stats(uuid))

        def _requeue_onlineplayers(self, resp: OnlinePlayersResponse) -> None:
            self._request_list.enqueue(
                resp.headers.expires.to_datetime().timestamp(),
                self._api.player.get_online_uuids(),
                priority=500
            )

        # PlayerResponse
        def _process_player_response(self, resps: Iterable[PlayerResponse]) -> None:
            logged_on_guilds: set[str] = set()
            for resp in resps:
                if resp.body.guild is None:
                    continue

                guild_name = resp.body.guild.name
                is_online = resp.body.online
                uuid = resp.body.uuid.uuid

                # If an uuid is online, and not in dictionary, create a new guild entry with the uuid.
                # This also means that the guild is LOGGED ON
                if is_online is True:
                    if guild_name not in self.online_guilds:
                        self.online_guilds[guild_name] = {uuid,}
                        logged_on_guilds.add(guild_name)
                    else:
                        # If guild is not LOGGED ON, add the uuid to the online uuids of that guild
                        self.online_guilds[guild_name].add(uuid)

                # If an uuid is offline, and in dictionary, remove the uuid from the set of that guild
                if (is_online is False) and (guild_name in self.online_guilds) and (uuid in self.online_guilds[guild_name]):
                    self.online_guilds[guild_name].remove(uuid)

                    # Check the guild dictionary, if the set is empty, remove the guild from the dictionary.
                    # This also means that the guild is LOGGED OFF
                    if len(self.online_guilds[guild_name]) == 0:
                        del self.online_guilds[guild_name]

            self._logged_on_guilds = logged_on_guilds.copy()

        def _enqueue_guild(self) -> None:
            for guild_name in self._logged_on_guilds:
                self._request_list.enqueue(0, self._api.guild.get(guild_name))

        def _requeue_player(self, resps: Iterable[PlayerResponse]) -> None:
            for resp in resps:
                if resp.body.online is False:
                    continue

                self._request_list.enqueue(
                    resp.headers.expires.to_datetime().timestamp(),  # due to ratelimit
                    self._api.player.get_full_stats(resp.body.uuid.uuid)
                )

        # GuildResponse
        def _requeue_guild(self, resps: Iterable[GuildResponse]) -> None:
            for resp in resps:
                if resp.body.members.get_online_members() <= 0:
                    continue

                self._request_list.enqueue(
                    resp.headers.expires.to_datetime().timestamp(),
                    self._api.guild.get(resp.body.name)
                )

        @property
        def logged_on_guilds(self) -> set[str]:
            """ Set of latest logged on guilds' names. """
            return self._logged_on_guilds

        @property
        def logged_on_players(self) -> set[str]:
            """ Set of latest logged on players' uuids. Needed by PlayerActivityHistory. """
            return self._logged_on_players

        @property
        def online_players(self) -> dict[str, datetime]:
            """ Dict of online players' uuids, paired with their logged on timestamp. """
            return self._online_players

        @property
        def online_guilds(self) -> dict[str, set[str]]:
            """ guild_name: set(online_uuids) """
            return self._online_guilds
