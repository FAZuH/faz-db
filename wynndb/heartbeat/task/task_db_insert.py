from __future__ import annotations
import asyncio
from datetime import datetime
from typing import TYPE_CHECKING, Iterable

from .task import Task
from wynndb.api.wynn.response import GuildResponse, PlayerResponse, OnlinePlayersResponse
from wynndb.adapter import ApiResponseAdapter
from wynndb.db.wynndb.model import KansUptime

if TYPE_CHECKING:
    from . import RequestQueue, ResponseQueue
    from wynndb import Api, Database, Logger


class TaskDbInsert(Task):
    """Inserts API responses to database."""

    def __init__(
        self,
        api: Api,
        db: Database,
        logger: Logger,
        request_list: RequestQueue,
        response_list: ResponseQueue,
    ) -> None:
        self._api = api
        self._db = db
        self._logger = logger
        self._request_list = request_list
        self._response_list = response_list

        self._event_loop = asyncio.new_event_loop()
        self._latest_run = datetime.now()
        self._response_adapter = ApiResponseAdapter()
        self._response_handler = self._ResponseHandler(self._api, self._request_list)
        self._start_time = datetime.now()

    def setup(self) -> None:
        self._event_loop.run_until_complete(self._db.create_all())
        # NOTE: Initial request. Results in a chain reaction of requests.
        self._request_list.enqueue(0, self._api.player.get_online_uuids(), priority=500)

    def teardown(self) -> None: ...

    def run(self) -> None:
        try:
            self._event_loop.run_until_complete(self._run())
        except Exception as e:
            self._event_loop.create_task(self._logger.discord.exception(f"Error inserting to database", e))
        self._latest_run = datetime.now()

    async def _run(self) -> None:
        await self._db.kans_uptime_repository.insert((KansUptime(self._start_time, datetime.now()),))

        online_players_resp: None | OnlinePlayersResponse = None
        player_resps: list[PlayerResponse] = []
        guild_resps: list[GuildResponse] = []
        for resp in self._response_list.get():
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

        if online_players_resp is not None:
            await self._insert_online_players_response(online_players_resp)
        if player_resps:
            await self._insert_player_responses(player_resps)
        if guild_resps:
            await self._insert_guild_response(guild_resps)

    async def _insert_online_players_response(self, resp: OnlinePlayersResponse) -> None:
        await self._db.online_players_repository.insert(self._response_adapter.OnlinePlayers.to_online_players(resp))
        await self._db.player_activity_history_repository.insert(
                self._response_adapter.OnlinePlayers.to_player_activity_history(
                        resp,
                        self._response_handler.online_players
                )
        )

    async def _insert_player_responses(self, resps: list[PlayerResponse]) -> None:
        character_history = []
        character_info = []
        player_history = []
        player_info = []
        for resp in resps:
            character_history.extend(self._response_adapter.Player.to_character_history(resp))
            character_info.extend(self._response_adapter.Player.to_character_info(resp))
            player_history.append(self._response_adapter.Player.to_player_history(resp))
            player_info.append(self._response_adapter.Player.to_player_info(resp))

        await self._db.player_info_repository.insert(player_info)
        await self._db.character_info_repository.insert(character_info)
        await self._db.player_history_repository.insert(player_history)
        await self._db.character_history_repository.insert(character_history)

    async def _insert_guild_response(self, resps: list[GuildResponse]) -> None:
        guild_info = []
        guild_history = []
        guild_member_history = []
        for resp in resps:
            guild_info.append(self._response_adapter.Guild.to_guild_info(resp))
            guild_history.append(self._response_adapter.Guild.to_guild_history(resp))
            guild_member_history.extend(self._response_adapter.Guild.to_guild_member_history(resp))

        await self._db.guild_info_repository.insert(guild_info)
        await self._db.guild_history_repository.insert(guild_history)
        await self._db.guild_member_history_repository.insert(guild_member_history)

    @property
    def response_handler(self) -> TaskDbInsert._ResponseHandler:
        return self._response_handler

    @property
    def first_delay(self) -> float:
        return 1.0

    @property
    def interval(self) -> float:
        return 5.0

    @property
    def latest_run(self) -> datetime:
        return self._latest_run

    @property
    def name(self) -> str:
        return self.__class__.__name__


    class _ResponseHandler:
        """Handles Wynncraft response processing, queueing, and requeuing."""

        def __init__(self, api: Api, request_list: RequestQueue) -> None:
            self._api = api
            self._request_list = request_list

            self._online_guilds: dict[str, set[str]] = {}
            self._online_players: dict[str, datetime] = {}
            self._logged_on_guilds: set[str] = set()
            self._logged_on_players: set[str] = set()

        def handle_onlineplayers_response(self, resp: None | OnlinePlayersResponse) -> None:
            if resp is None:
                return
            self._process_onlineplayers_response(resp)
            self._requeue_onlineplayers(resp)
            self._enqueue_player()

        def handle_player_response(self, resps: Iterable[PlayerResponse]) -> None:
            self._process_player_response(resps)
            self._requeue_player(resps)
            self._enqueue_guild()

        def handle_guild_response(self, resps: Iterable[GuildResponse]) -> None:
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
            """Set of latest logged on guilds' names."""
            return self._logged_on_guilds

        @property
        def logged_on_players(self) -> set[str]:
            """Set of latest logged on players' uuids. Needed by PlayerActivityHistory."""
            return self._logged_on_players

        @property
        def online_players(self) -> dict[str, datetime]:
            """Dict of online players' uuids, paired with their logged on timestamp."""
            return self._online_players

        @property
        def online_guilds(self) -> dict[str, set[str]]:
            """guild_name: set(online_uuids)"""
            return self._online_guilds
