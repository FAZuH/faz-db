from dataclasses import asdict
from time import perf_counter, time
from typing import *  # type: ignore
# TODO: Do proper import

from discord.ext.tasks import loop

from database.vindicator_database import VindicatorDatabase
from objects.database import (
    GuildMainInfo,
    GuildMain,
    GuildMember,
)
from request.fetch_player import FetchPlayer
from request.wynncraft_request import WynncraftRequest
from constants import FETCH_GUILD_INTERVAL, DatabaseTables
from utils.wynncraft_response_utils import WynncraftResponseUtils as WynnUtils

if TYPE_CHECKING:
    from aiohttp import ClientResponse

    from objects.wynncraft_response import GuildStats, PlayerStats

FetchedGuild = TypedDict("FetchedGuild", {"response_timestamp": float, "guild_stats": "GuildStats"})


class FetchGuild:

    guild_list: List[str] = []
    fetch_queue: Dict[str, float] = {}
    fetched_guilds: List[FetchedGuild] = []
    fetching: bool = False
    timestamp: float
    requeue_schedule: Dict[str, float] = {}

    @classmethod
    @loop(seconds=FETCH_GUILD_INTERVAL)
    async def run(cls):
        t0: float = perf_counter()
        # await cls._request_api()
        # await cls._update_fetch_queue()

        if not cls.fetching:
            await cls._fetch_guilds()
            await cls._to_db()

        td: float = perf_counter() - t0

    @classmethod
    async def _request_api(cls) -> None:
        cls.guild_list = [record["name"] for record in await WynncraftRequest.get_guild_list_json()]
        cls.timestamp = time()

    @classmethod
    async def _update_fetch_queue(cls) -> None:
        """Updates cls.fetch_queue"""
        # Adds online_guilds into fetch queue
        for player_stat in FetchPlayer.latest_fetch.copy():
            guild_name: str = player_stat[1]["guild"]["name"]
            if guild_name in cls.fetch_queue:
                continue

            cls.fetch_queue[guild_name] = time()

        # Requeues fetched guilds (if passed schedule time)
        for guild_name, requeue_time in cls.requeue_schedule.copy().items():
            if guild_name in cls.fetch_queue or requeue_time > time():
                continue

            cls.fetch_queue[guild_name] = cls.requeue_schedule.pop(guild_name)  # Requeue


        # Adds guilds that's not saved in database yet
        query: str = f"SELECT name FROM {DatabaseTables.GUILD_MAIN_INFO}"
        saved_guild_names: List[str] = [record["name"] for record in await VindicatorDatabase.read_all(query)]
        for guild_name in cls.guild_list:
            if guild_name in cls.fetch_queue or guild_name in saved_guild_names:
                continue

            cls.fetch_queue[guild_name] = time()

    @classmethod
    async def _fetch_guilds(cls):
        """Requests guild stats from Wynncraft API. Saves into cls.fetched_guilds

        Guilds-to-fetch are grabbed from:
        - _latest_fetch class variable of FetchPlayer class
        - guilds that's not saved in database
        """
        fetch_queue: Dict[str, float] = cls.fetch_queue.copy()
        cls.fetch_queue.clear()  #
        cls.fetched_guilds.clear()  #
        guilds_to_fetch: List[str] = [guild_name for guild_name, _ in sorted(fetch_queue.items(), key=lambda item: item[1])]  # Get guild names sorted by timestamp

        guilds_to_fetch = ["WynnContentTeam", "Holders Of LE", "Wynn Theory"]

        cls.fetching = True
        # t0: float = perf_counter()
        # temp: int = len(guilds_to_fetch)
        # excs: int = 0
        # print("Fetching", temp, "guilds...")
        while guilds_to_fetch:
            concurrent_request: int = 25
            guilds_to_fetch_ = guilds_to_fetch[:concurrent_request]  # Poll
            guilds_to_fetch = guilds_to_fetch[concurrent_request:]  # Update queue

            guild_stat_resps: List["ClientResponse"] = await WynncraftRequest.get_many_guild_stats_response(guilds_to_fetch_)
            # excs += (len(guilds_to_fetch_) - len(guild_stat_resps))
            # print("Fetched", len(guild_stat_resps), "guilds")

            for response in guild_stat_resps:
                response_dt: float = WynnUtils.parse_datestr1(response.headers.get("Date", ""))
                guild_stat: "GuildStats" = await response.json()
                cls.fetched_guilds.append({"response_timestamp": response_dt, "guild_stats": guild_stat})
                cls.requeue_schedule[guild_stat["name"]] = response_dt + FETCH_GUILD_INTERVAL

            # print(f"{perf_counter() - t0:.2f} | {len(cls.fetched_guilds)} out of {temp} guilds fetched. {len(guilds_to_fetch)} left.\n")

        with open(f"{int(time())}guilds.json", "w") as f:
            import json
            json.dump(cls.fetched_guilds, f, indent=4)
        # t0=perf_counter()
        # for guild in guilds_to_fetch.copy():
        #     t1=perf_counter()
        #     cls.fetched_guilds.append((time(), await WynncraftAPIRequest.get_guild_stats_json(guild)))

        cls.fetching = False

    @classmethod
    async def _to_db(cls):
        import json
        with open("1699075292guilds.json") as f:
            data: List["FetchedGuild"] = json.load(f)

        # TODO: to_database:
        # guild_main_info = GuildMainInfo.from_raw(data)  # - guild_main_info
        # guild_main = GuildMain.from_raw(data)  # - guild_main
        # guild_member = GuildMember.from_raw(data)  # - guild_member
        # raw_online_guild = RawOnlineGuild.from_raw(data)  # raw_online_guild
        # raw_recent_guild = RawRecentGuild.from_raw(data) # raw_recent_guild

        # await GuildMainInfo.to_db(guild_main_info)
        # await GuildMain.to_db(guild_main)
        # await GuildMember.to_db(guild_member)
        # await RawOnlineGuild.to_db(raw_online_guild)
        # await RawRecentGuild.to_db(raw_recent_guild)
