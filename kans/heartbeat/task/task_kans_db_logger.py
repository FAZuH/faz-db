from __future__ import annotations
import asyncio
from datetime import datetime as dt
from typing import TYPE_CHECKING, Generator, Iterable

from .task import Task
from kans.api.wynn.response import GuildResponse, PlayerResponse, OnlinePlayersResponse
from kans.db.model import (
    CharacterHistory,
    CharacterInfo,
    GuildHistory,
    GuildInfo,
    GuildMemberHistory,
    KansUptime,
    OnlinePlayers,
    PlayerActivityHistory,
    PlayerHistory,
    PlayerInfo,
)

if TYPE_CHECKING:
    from datetime import datetime as dt
    from loguru import Logger
    from . import RequestList, ResponseList
    from kans.api import Api
    from kans.db import Database


class TaskKansDbLogger(Task):  # TODO: find better name
    """implements `TaskBase`"""

    def __init__(
        self,
        logger: Logger,
        api: Api,
        db: Database,
        request_list: RequestList,
        response_list: ResponseList
    ) -> None:
        self._logger = logger
        self._api = api
        self._db = db
        self._request_list = request_list
        self._response_list = response_list

        self._event_loop = asyncio.new_event_loop()
        self._online_players_manager = _OnlinePlayersManager()
        self._converter = _Converter(self._online_players_manager)
        self._online_guilds_manager = _OnlineGuildsManager()
        self._start_time = dt.now()

        self._request_list.put(0, self._api.player.get_online_uuids)

    def setup(self) -> None: ...
    def teardown(self) -> None: ...

    def run(self) -> None:
        self._event_loop.run_until_complete(self._run())

    async def _run(self) -> None:
        await self._db.kans_uptime_repository.insert((KansUptime(self._start_time, dt.now()),))

        player_resps: list[PlayerResponse] = []
        guild_resps: list[GuildResponse] = []
        for resp in self._response_list.get():
            if isinstance(resp, PlayerResponse):
                player_resps.append(resp)
            elif isinstance(resp, OnlinePlayersResponse):
                await self._handle_players_response(resp)
            elif isinstance(resp, GuildResponse):
                guild_resps.append(resp)

        if player_resps:
            await self._handle_player_responses(player_resps)
        if guild_resps:
            await self._handle_guild_response(guild_resps)

    async def _handle_players_response(self, resp: OnlinePlayersResponse) -> None:
        online_players: list[OnlinePlayers] = []
        player_activity_history: list[PlayerActivityHistory] = []

        logged_on: set[str] = self._online_players_manager.run(resp)

        # Queue new
        for uuid in logged_on:
            self._request_list.put(0, self._api.player.get_full_stats, uuid)

        # Requeue
        self._request_list.put(resp.get_expiry_datetime().timestamp(), self._api.player.get_online_uuids, priority=0)

        # Create DB models
        online_players.extend(self._converter.to_online_players((resp,)))
        player_activity_history.extend(self._converter.to_player_activity_history((resp,), logged_on))

        # Insert to DB
        await self._db.online_players_repository.insert(online_players)
        await self._db.player_activity_history_repository.insert(player_activity_history)

    async def _handle_player_responses(self, resps: list[PlayerResponse]) -> None:
        logged_on_guilds = self._online_guilds_manager.run(resps)

        # Queue new
        for guild_name in logged_on_guilds:
            self._request_list.put(0, self._api.guild.get, guild_name)  # Timestamp doesn't matter here

        character_history: list[CharacterHistory] = []
        character_info: list[CharacterInfo] = []
        player_history: list[PlayerHistory] = []
        player_info: list[PlayerInfo] = []
        for resp in resps:
            # Requeue
            if resp.body.online is True:
                self._request_list.put(
                        resp.get_expiry_datetime().timestamp() + 480,  # due to ratelimit
                        self._api.player.get_full_stats,
                        resp.body.uuid.uuid
                )

            # Create DB models
            character_history.extend(self._converter.to_character_history((resp,)))
            character_info.extend(self._converter.to_character_info((resp,)))
            player_history.extend(self._converter.to_player_history((resp,)))
            player_info.extend(self._converter.to_player_info((resp,)))

        # Insert to DB
        await self._db.player_info_repository.insert(player_info)
        await self._db.character_info_repository.insert(character_info)
        await self._db.player_history_repository.insert(player_history)
        await self._db.character_history_repository.insert(character_history)

    async def _handle_guild_response(self, resps: list[GuildResponse]) -> None:
        guild_info = []
        guild_history = []
        guild_member_history = []
        for resp in resps:
            # Requeue
            if resp.body.members.get_online_members() > 0:
                self._request_list.put(
                        resp.get_expiry_datetime().timestamp(),
                        self._api.guild.get,
                        resp.body.name
                )

            # Create DB models
            guild_info.extend(self._converter.to_guild_info((resp,)))
            guild_history.extend(self._converter.to_guild_history((resp,)))
            guild_member_history.extend(self._converter.to_guild_member_history((resp,)))

        # Insert to Db
        await self._db.guild_info_repository.insert(guild_info)
        await self._db.guild_history_repository.insert(guild_history)
        await self._db.guild_member_history_repository.insert(guild_member_history)

    @property
    def first_delay(self) -> float:
        return 1.0

    @property
    def interval(self) -> float:
        return 5.0

    @property
    def name(self) -> str:
        return "WynndataLogger"


class _OnlinePlayersManager:
    """Handles computing new online player responses."""

    def __init__(self) -> None:
        self._logon_timestamps: dict[str, dt] = {}
        self._prev_online_uuids: set[str] = set()

    def run(self, resp: OnlinePlayersResponse) -> set[str]:
        online_uuids: set[str] = {str(uuid) for uuid in resp.body.players}
        logged_off: set[str] = self._prev_online_uuids - online_uuids
        logged_on: set[str] = online_uuids - self._prev_online_uuids
        self._prev_online_uuids = online_uuids.copy()

        for uuid in logged_off:
            del self._logon_timestamps[uuid]

        for uuid in logged_on:
            self._logon_timestamps[uuid] = resp.get_datetime()

        return logged_on

    @property
    def logon_timestamps(self) -> dict[str, dt]:
        return self._logon_timestamps

    @property
    def prev_online_uuids(self) -> set[str]:
        return self._prev_online_uuids


class _OnlineGuildsManager:
    """Handles computing new online guild responses."""

    def __init__(self) -> None:
        self._prev_online_guilds: set[str] = set()

    def run(self, resps: Iterable[PlayerResponse]) -> set[str]:
        # internal data processing
        online_guilds: set[str] = {resp.body.guild.name for resp in resps if resp.body.guild is not None}
        logged_on: set[str] = self._prev_online_guilds - online_guilds
        self._prev_online_guilds = online_guilds.copy()
        return logged_on


class _Converter:
    """Converts wynncraft API responses to DB models."""

    def __init__(self, online_players_manager: _OnlinePlayersManager) -> None:
        self._online_players_manager = online_players_manager

    def to_character_history(self, resps: Iterable[PlayerResponse]) -> Generator[CharacterHistory, None, None]:
        return (CharacterHistory(
                character_uuid=ch_uuid.to_bytes(),
                level=ch.level,
                xp=ch.xp,
                wars=ch.wars,
                playtime=ch.playtime,
                mobs_killed=ch.mobs_killed,
                chests_found=ch.chests_found,
                logins=ch.logins,
                deaths=ch.deaths,
                discoveries=ch.discoveries,
                gamemode=ch.gamemode.to_bytes(),
                alchemism=ch.professions.alchemism.to_decimal(),
                armouring=ch.professions.armouring.to_decimal(),
                cooking=ch.professions.cooking.to_decimal(),
                jeweling=ch.professions.jeweling.to_decimal(),
                scribing=ch.professions.scribing.to_decimal(),
                tailoring=ch.professions.tailoring.to_decimal(),
                weaponsmithing=ch.professions.weaponsmithing.to_decimal(),
                woodworking=ch.professions.woodworking.to_decimal(),
                mining=ch.professions.mining.to_decimal(),
                woodcutting=ch.professions.woodcutting.to_decimal(),
                farming=ch.professions.farming.to_decimal(),
                fishing=ch.professions.fishing.to_decimal(),
                dungeon_completions=ch.dungeons.total,
                quest_completions=len(ch.quests),
                raid_completions=ch.raids.total,
                datetime=resp.get_datetime()
        ) for resp in resps for ch_uuid, ch in resp.body.iter_characters())

    def to_character_info(self, resps: Iterable[PlayerResponse]) -> Generator[CharacterInfo, None, None]:
        return (CharacterInfo(
                character_uuid=character_uuid.to_bytes(),
                uuid=resp.body.uuid.to_bytes(),
                type=character.type.get_kind()
        ) for resp in resps for character_uuid, character in resp.body.iter_characters())

    def to_guild_history(self, resps: Iterable[GuildResponse]) -> Generator[GuildHistory, None, None]:
        return (GuildHistory(
                name=resp.body.name,
                level=resp.body.level,
                territories=resp.body.territories,
                wars=resp.body.wars,
                member_total=resp.body.members.total,
                online_members=resp.body.members.get_online_members(),
                datetime=resp.get_datetime()
        ) for resp in resps)

    def to_guild_info(self, resps: Iterable[GuildResponse]) -> Generator[GuildInfo, None, None]:
        return (GuildInfo(
                name=resp.body.name,
                prefix=resp.body.prefix,
                created=resp.body.created.to_datetime()
        ) for resp in resps)

    def to_guild_member_history(self, resps: Iterable[GuildResponse]) -> Generator[GuildMemberHistory, None, None]:
        return (GuildMemberHistory(
                uuid=uuid.to_bytes() if uuid.is_uuid() else memberinfo.uuid.to_bytes(),  # type: ignore
                contributed=memberinfo.contributed,
                joined=memberinfo.joined.to_datetime(),
                datetime=resp.get_datetime()
        ) for resp in resps for rank, uuid, memberinfo in resp.body.members.iter_online_members())  # type: ignore

    def to_online_players(self, resps: Iterable[OnlinePlayersResponse]) -> Generator[OnlinePlayers, None, None]:
        return (
                OnlinePlayers(uuid=uuid.to_bytes(), server=server)
                for resp in resps
                for uuid, server in resp.body.iter_players()
        )

    def to_player_activity_history(self, resps: Iterable[OnlinePlayersResponse], logged_on: set[str]) -> Generator[PlayerActivityHistory, None, None]:
        return (
                PlayerActivityHistory(
                        uuid.username_or_uuid,
                        self._online_players_manager.logon_timestamps[uuid.username_or_uuid],
                        resp.get_datetime()
                )
                for resp in resps
                for uuid in resp.body.players
                if (uuid.is_uuid() and uuid.username_or_uuid in logged_on)
        )

    def to_player_history(self, resps: Iterable[PlayerResponse]) -> Generator[PlayerHistory, None, None]:
        return (PlayerHistory(
                uuid=resp.body.uuid.to_bytes(),
                username=resp.body.username,
                support_rank=resp.body.support_rank,
                playtime=resp.body.playtime,
                guild_name=resp.body.guild.name if resp.body.guild else None,
                guild_rank=resp.body.guild.rank if resp.body.guild else None,
                rank=resp.body.rank,
                datetime=resp.get_datetime()
        ) for resp in resps)

    def to_player_info(self, resps: Iterable[PlayerResponse]) -> Generator[PlayerInfo, None, None]:
        return (PlayerInfo(
                uuid=resp.body.uuid.to_bytes(),
                latest_username=resp.body.username,
                first_join=resp.body.first_join.to_datetime()
        ) for resp in resps)
