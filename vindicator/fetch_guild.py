from __future__ import annotations
from time import time

from discord.ext.tasks import loop

from vindicator import (
    GuildStats,
    FetchPlayer,
    GuildMainInfoUtil,
    GuildMainUtil,
    GuildMemberUtil,
    Logger,
    WynncraftRequest,
    WynncraftResponseUtil,
)
from vindicator.constants import *
from vindicator.typehints import *


class FetchGuild:

    _fetch_queue: Dict[str, float] = {}
    _latest_fetch: List[FetchedGuild] = []
    _requeue_schedule: Dict[str, float] = {}
    _is_running: bool = False


    @classmethod
    @loop(seconds=FETCH_GUILD_INTERVAL)
    @Logger.logging_decorator
    async def run(cls) -> None:
        if not cls._is_running:
            cls._is_running = True
            await cls._run()
            cls._is_running = False

    @classmethod
    async def _run(cls):
        await cls._update_fetch_queue()
        if cls._fetch_queue:
            await cls._fetch_guilds()
            await cls._to_db()


    @classmethod
    async def _update_fetch_queue(cls) -> None:
        for player_stats in FetchPlayer.get_latest_fetch():
            try:
                guild_name: str = player_stats["player_stats"]["guild"]["name"]
                if guild_name not in cls._fetch_queue:
                    cls._fetch_queue[guild_name] = time()
            except (KeyError, TypeError):
                continue  # if field doesn't exist in response

        for guild_name, requeue_time in cls._requeue_schedule.copy().items():
            if guild_name not in cls._fetch_queue and requeue_time <= time():
                cls._fetch_queue[guild_name] = cls._requeue_schedule.pop(guild_name)

    @classmethod
    async def _fetch_guilds(cls):
        """Requests guild stats from Wynncraft API. Saves into cls.fetched_guilds."""
        fethed_guilds: List[FetchedGuild] = []
        fetch_queue: Dict[str, float] = cls._fetch_queue.copy()
        guilds_to_fetch: List[str] = [guild_name for guild_name, _ in sorted(fetch_queue.items(), key=lambda item: item[1])]  # Get guild names sorted by timestamp
        cls._fetch_queue.clear()  #

        concurrent_request: int = 50
        excs: List[BaseException] = []
        excs_: List[BaseException]
        ress: List[ResponseSet[GuildStats, Headers]] = []
        ress_: List[ResponseSet[GuildStats, Headers]]

        async with WynncraftRequest() as client:
            while guilds_to_fetch:
                excs_, ress_ = await client.get_many_guild_stats(guilds_to_fetch[:concurrent_request])
                guilds_to_fetch = guilds_to_fetch[concurrent_request:]  # dequeue
                excs.extend(excs_)
                ress.extend(ress_)
                # TODO: log exceptions

        for r in ress:
            fethed_guilds.append({"resp_datetime": WynncraftResponseUtil.resp_to_sqldt(r.headers.get("Date", "")), "guild_stats": r.json})
            cls._requeue_schedule[r.json["name"]] = WynncraftResponseUtil.resp_to_timestamp(r.headers.get("Expires", ""))

        cls._latest_fetch = fethed_guilds.copy()

    @classmethod
    async def _to_db(cls):
        fethed_guilds: List[FetchedGuild] = cls._latest_fetch.copy()
        await GuildMainInfoUtil(fethed_guilds).to_db()
        await GuildMainUtil(fethed_guilds).to_db()
        await GuildMemberUtil(fethed_guilds).to_db()
