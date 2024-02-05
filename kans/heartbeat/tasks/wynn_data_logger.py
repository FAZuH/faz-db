from __future__ import annotations
import asyncio
from threading import Lock
from typing import TYPE_CHECKING, Any, Generator

from kans import (
    CharacterHistory,
    CharacterInfo,
    GuildHistory,
    GuildInfo,
    GuildMemberHistory,
    GuildResponse,
    OnlinePlayers,
    PlayerActivityHistory,
    PlayerHistory,
    PlayerInfo,
    PlayerResponse,
    PlayersResponse,
    TaskBase,
)

if TYPE_CHECKING:
    from datetime import datetime as dt
    from loguru import Logger
    from kans import (
        Database,
        Player,
        RequestQueue,
        WynnApi,
        WynnResponse,
    )


class WynnDataLogger(TaskBase):  # TODO: find better name
    """implements `TaskBase`"""

    def __init__(
        self,
        logger: Logger,
        wynnapi: WynnApi,
        wynnrepo: Database,
        request_queue: RequestQueue
    ) -> None:
        self._logger = logger
        self._wynnapi = wynnapi
        self._wynnrepo = wynnrepo
        self._request_queue = request_queue

        self._event_loop = asyncio.new_event_loop()
        self._response_lock = Lock()
        self._responses = []

        self._prev_online_guilds: set[str] = set()
        self._logon_timestamps: dict[str, dt] = {}
        self._prev_online_uuids: set[str] = set()

        self._request_queue.put(0, self._wynnapi.get_online_uuids)

    def run(self) -> None:
        self._event_loop.run_until_complete(self._run())

    def put_response(self, response: WynnResponse[Any]) -> None:
        with self._response_lock:
            self._responses.append(response)

    def popall_responses(self) -> Generator[WynnResponse[Any], Any, None]:
        with self._response_lock:
            while len(self._responses) > 0:
                yield self._responses.pop()

    async def _run(self) -> None:
        player_resps: list[PlayerResponse] = []
        players_resps: list[PlayersResponse] = []
        guild_resps: list[GuildResponse] = []

        for resp in self.popall_responses():
            if isinstance(resp, PlayerResponse):
                player_resps.append(resp)
            elif isinstance(resp, PlayersResponse):
                players_resps.append(resp)
            elif isinstance(resp, GuildResponse):
                guild_resps.append(resp)

        async with asyncio.TaskGroup() as tg:
            t1 = tg.create_task(self._handle_player_responses(player_resps))
            t2 = tg.create_task(self._handle_players_response(players_resps))
            t3 = tg.create_task(self._handle_guild_response(guild_resps))

        res = [t1, t2, t3]
        for r in res:
            if r.done() and r.exception():
                await r

    async def _handle_player_responses(self, resps: list[PlayerResponse]) -> None:
        if len(resps) == 0:
            return

        # internal data processing
        online_guilds: set[str] = set()  # placeholder for new self._prev_online_guilds data
        logged_on_guilds: set[str] = set()
        for resp in resps:
            player: Player = resp.body
            if player.guild is None:
                continue

            guild_name: str = player.guild.name

            online_guilds.add(guild_name)
            if guild_name not in self._prev_online_guilds:
                logged_on_guilds.add(guild_name)

        self._prev_online_guilds = online_guilds.copy()

        # to db
        await self._wynnrepo.player_info_repository.insert(PlayerInfo.from_responses(resps))
        await self._wynnrepo.character_info_repository.insert(CharacterInfo.from_responses(resps))
        await self._wynnrepo.player_history_repository.insert(PlayerHistory.from_responses(resps))
        await self._wynnrepo.character_history_repository.insert(CharacterHistory.from_responses(resps))

        for resp in resps:
            # requeue if player is online
            if resp.body.online is True:
                self._request_queue.put(
                    resp.get_expiry_datetime().timestamp() + 480,  # due to ratelimit
                    self._wynnapi.get_player_stats,
                    resp.body.uuid.uuid
                )

        # queue newly logged on guilds
        for guild_name in logged_on_guilds:
            # Timestamp doesn't matter here
            self._request_queue.put(0, self._wynnapi.get_guild_stats, guild_name)

    async def _handle_players_response(self, resps: list[PlayersResponse]) -> None:
        if len(resps) == 0:
            return

        for resp in resps:
            # internal data processing
            online_uuids: set[str] = {str(uuid) for uuid in resp.body.players}

            logged_off: set[str] = self._prev_online_uuids - online_uuids
            logged_on: set[str] = online_uuids - self._prev_online_uuids

            self._prev_online_uuids = online_uuids.copy()

            for uuid in logged_off:
                del self._logon_timestamps[uuid]

            for uuid in logged_on:
                self._logon_timestamps[uuid] = resp.get_datetime()

            # queue newly logged on players
            for uuid in logged_on:
                self._request_queue.put(
                    0,
                    self._wynnapi.get_player_stats,
                    uuid
                )

            # to db
            playeractivityhistory = tuple(
                PlayerActivityHistory(
                    uuid.username_or_uuid,
                    self._logon_timestamps[uuid.username_or_uuid],
                    resp.get_datetime()
                )
                for uuid in resp.body.players
                if (uuid.is_uuid() and uuid.username_or_uuid in logged_on)
            )
            await self._wynnrepo.online_players_repository.insert(OnlinePlayers.from_response(resp))
            await self._wynnrepo.player_activity_history_repository.insert(playeractivityhistory)

            # always requeue
            self._request_queue.put(resp.get_expiry_datetime().timestamp(), self._wynnapi.get_online_uuids)

    async def _handle_guild_response(self, resps: list[GuildResponse]) -> None:
        if len(resps) == 0:
            return

        # to db
        await self._wynnrepo.guild_info_repository.insert(GuildInfo.from_responses(resps))
        await self._wynnrepo.guild_history_repository.insert(GuildHistory.from_responses(resps))
        await self._wynnrepo.guild_member_history_repository.insert(GuildMemberHistory.from_responses(resps))

        # requeue if there's online members in guild
        for resp in resps:
            if resp.body.members.get_online_members() > 0:
                self._request_queue.put(
                    resp.get_expiry_datetime().timestamp(),
                    self._wynnapi.get_guild_stats,
                    resp.body.name
                )

    @property
    def first_delay(self) -> float:
        return 1.0

    @property
    def interval(self) -> float:
        return 5.0

    @property
    def name(self) -> str:
        return "WynnDataLogger"
