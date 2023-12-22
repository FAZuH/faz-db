from __future__ import annotations
from asyncio import create_task
from time import perf_counter, time
from typing import TYPE_CHECKING, Dict, List

from discord.ext.tasks import loop

from vindicator import (
    FETCH_GUILD_INTERVAL,
    GuildStats,
    DatabaseTables,
    FetchPlayer,
    GuildMainInfo,
    GuildMain,
    GuildMember,
    VindicatorWebhook,
    WynncraftRequest,
    WynncraftResponseUtils,
)

if TYPE_CHECKING:
    from aiohttp import ClientResponse
    from vindicator.types import *


class FetchGuild:

    _online_guilds: List[str] = []
    _fetch_queue: Dict[str, float] = {}
    _fetched_guilds: List[FetchedGuild] = []
    _fetching: bool = False
    _latest_fetch: List[FetchedGuild] = []
    _timestamp: float
    _requeue_schedule: Dict[str, float] = {}

    @classmethod
    @loop(seconds=FETCH_GUILD_INTERVAL)
    async def run(cls):
        t0: float = perf_counter()  # TODO: webhook logging

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
            except Exception:
                # if field doesn't exist in response
                continue  # TODO: do proper exception handling

        for guild_name, requeue_time in cls._requeue_schedule.copy().items():
            if guild_name not in cls._fetch_queue and requeue_time <= time():
                cls._fetch_queue[guild_name] = cls._requeue_schedule.pop(guild_name)

    @classmethod
    async def _fetch_guilds(cls):
        """Requests guild stats from Wynncraft API. Saves into cls.fetched_guilds

        Guilds-to-fetch are grabbed from:
        - _latest_fetch class variable of FetchPlayer class
        """
        fetch_queue: Dict[str, float] = cls._fetch_queue.copy()
        guilds_to_fetch: List[str] = [guild_name for guild_name, _ in sorted(fetch_queue.items(), key=lambda item: item[1])]  # Get guild names sorted by timestamp
        cls._fetch_queue.clear()  #
        cls._fetched_guilds.clear()  #

        concurrent_request: int = 50
        excs: List[BaseException] = []
        excs_: List[BaseException]
        resps: List[ClientResponse] = []
        resps_: List[ClientResponse]

        t0: float = perf_counter()
        async with WynncraftRequest._rm.session as s:
            while guilds_to_fetch:
                excs_, resps_ = await WynncraftRequest.get_many_guild_stats_response(s, guilds_to_fetch[:concurrent_request])
                guilds_to_fetch = guilds_to_fetch[concurrent_request:]
                excs.extend(excs_)
                resps.extend(resps_)

            for r in resps:
                resp_dt: float = WynncraftResponseUtils.parse_datestr1(r.headers.get("Date", ""))
                guild_stat: GuildStats = await r.json()

                cls._fetched_guilds.append({"response_timestamp": resp_dt, "guild_stats": guild_stat})
                cls._requeue_schedule[guild_stat["name"]] = WynncraftResponseUtils.parse_datestr1(r.headers.get("Expires", ""))

        t1: float = perf_counter()
        create_task(VindicatorWebhook.log("wynncraft_request", "request", {
            "fetched guilds": len(resps),
            "time spent": f"{t1-t0:.2f}s",
            "exceptions": len(excs),
        }, title="Fetch online guild stats"))
        cls._latest_fetch = cls._fetched_guilds.copy()

    @classmethod
    async def _to_db(cls):
        fethed_guilds: lFetchedGuilds = cls._latest_fetch.copy()
        t0: float = perf_counter()
        await GuildMainInfo.to_db(fethed_guilds); t1: float = perf_counter()
        await GuildMain.to_db(fethed_guilds); t2: float = perf_counter()
        await GuildMember.to_db(fethed_guilds); t3: float = perf_counter()

        create_task(VindicatorWebhook.log("database", "write", {
            "records": len(fethed_guilds),
            "table1": DatabaseTables.GUILD_MAIN_INFO,
            "time1": f"{t1-t0:.2f}s",
            "table2": DatabaseTables.GUILD_MAIN,
            "time2": f"{t2-t1:.2f}s",
            "table3": DatabaseTables.GUILD_MEMBER,
            "time3": f"{t3-t2:.2f}s",
        }, title="Save fetched guilds to database"))
