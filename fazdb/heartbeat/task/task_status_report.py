from __future__ import annotations
import asyncio
from datetime import datetime, timedelta
import platform
import psutil
from typing import TYPE_CHECKING

from aiohttp import ClientSession
import nextcord

from . import Task
from fazdb.app import Config

if TYPE_CHECKING:
    from . import RequestQueue, TaskApiRequest, TaskDbInsert
    from fazdb import Api, IFazdbDatabase, Logger


class TaskStatusReport(Task):
    # TODO: make tests later. this task is still bound to change.

    def __init__(
        self,
        logger: Logger,
        api: Api,
        api_request: TaskApiRequest,
        db: IFazdbDatabase,
        db_insert: TaskDbInsert,
        request_list: RequestQueue
    ) -> None:
        self._logger = logger
        self._api = api
        self._api_request = api_request
        self._db = db
        self._db_insert = db_insert
        self._request_list = request_list

        self._event_loop = asyncio.new_event_loop()
        self._latest_run = self._start_time = datetime.now()
        self._message_id: None | int = None
        self._url = Config.discord_status_webhook

    def setup(self) -> None:
        self._event_loop.run_until_complete(self.async_setup())

    def teardown(self) -> None: ...

    def run(self) -> None:
        self._event_loop.run_until_complete(self._run())
        self._latest_run = datetime.now()

    async def async_setup(self):
        async with ClientSession() as s:
            hook = nextcord.Webhook.from_url(self._url, session=s)
            await hook.edit(name="faz-db Information")
            await hook.send("Started faz-db.")
        perf = self._logger.performance
        self._api.guild.get = perf.bind_async(self._api.guild.get)
        self._api.guild.get_from_prefix = perf.bind_async(self._api.guild.get_from_prefix)
        self._api.player.get_full_stats = perf.bind_async(self._api.player.get_full_stats)
        self._api.player.get_online_uuids = perf.bind_async(self._api.player.get_online_uuids)

    async def _run(self) -> None:
        await self._send()

    async def _send(self) -> None:
        async with ClientSession() as s:
            hook = nextcord.Webhook.from_url(self._url, session=s)
            report = await self._get_report()

            if self._message_id is None:
                message = await hook.send(content=report, wait=True)
                self._message_id = message.id
            else:
                try:
                    message = await hook.fetch_message(self._message_id)
                except nextcord.DiscordException as e:
                    await self._logger.discord.exception("Failed to fetch message.", e)
                    self._message_id = None
                    return

                await message.edit(content=report)

    _DEFAULT_MSG = (
            "```yaml"
            "\n."
            "\n├── faz-db Stats/"
            "\n│   ├── Runtime : {}"
            "\n│   ├── RAM     : {:.2f} MB"
            "\n│   └── CPU     : {:.2f}%"
            "\n│"
            "\n├── Tasks/"
            "\n│   ├── ApiRequest Latest   : {}"
            "\n│   ├── DbInsert Latest     : {}"
            "\n│   ├── StatusReport Latest : {}"
            "\n│   └── RequestList/"
            "\n│       └── [ Queued | Eligible | Running ]/"
            "\n│           ├── GuildStat     : [ {:<4} | {:<4} | {:<4} ]"
            "\n│           ├── OnlinePlayers : [ {:<4} | {:<4} | {:<4} ]"
            "\n│           └── PlayerStat    : [ {:<4} | {:<4} | {:<4} ]"
            "\n│"
            "\n├── Api Stats/"
            "\n│   ├── Ratelimit      : {}"
            "\n│   ├── Online Players : {}"
            "\n│   ├── Online Guilds  : {}"
            "\n│   ├── Avg Guild Req Duration         : {:.2f}"
            "\n│   ├── Avg OnlinePlayers Req Duration : {:.2f}"
            "\n│   ├── Avg Player Req Duration        : {:.2f}"
            "\n│   ├── Guild Reqs Within 5m         : {}"
            "\n│   ├── OnlinePlayers Reqs Within 5m : {}"
            "\n│   ├── Player Reqs Within 5m        : {}"
            "\n│   └── All Reqs Within 5m           : {}"
            "\n│"
            "\n└── System Stats/"
            "\n    ├── OS     : {}"
            "\n    └── Uptime : {}"
            "\n```"
    )

    # TODO: clean code
    async def _get_report(self) -> str:
        now = datetime.now()
        now_ts = now.timestamp()

        unique_request_list = {
                "queued": [0, 0, 0],
                "eligible": [0, 0, 0],
                "running": [0, 0, 0]
        }
        match_qualname = {
                "PlayerEndpoint.get_full_stats": 0,
                "PlayerEndpoint.get_online_uuids": 1,
                "GuildEndpoint.get": 2
        }

        for req in self._request_list.iter():
            index = match_qualname.get(req.coro.__qualname__, 3)
            unique_request_list["queued"][index] += 1
            if req.is_eligible(now_ts):
                unique_request_list["eligible"][index] += 1

        for req in self._api_request.running_requests.copy():
            coro = req.get_coro()
            index = match_qualname.get(coro.__qualname__, 3)
            unique_request_list["running"][index] += 1

        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

        # TODO: hacky way to do these. change later
        avg_guild_req_duration = self._logger.performance.get_average("GuildEndpoint.get")
        avg_onlineplayers_req_duration = self._logger.performance.get_average("PlayerEndpoint.get_online_uuids")
        avg_player_req_duration = self._logger.performance.get_average("PlayerEndpoint.get_full_stats")

        recent_guild_reqs = len(self._logger.performance.get_recent(timedelta(minutes=5), "GuildEndpoint.get"))
        recent_onlineplayers_reqs = len(self._logger.performance.get_recent(timedelta(minutes=5), "PlayerEndpoint.get_online_uuids"))
        recent_player_reqs = len(self._logger.performance.get_recent(timedelta(minutes=5), "PlayerEndpoint.get_full_stats"))
        recent_all_reqs = recent_guild_reqs + recent_onlineplayers_reqs + recent_player_reqs

        msg = self._DEFAULT_MSG.format(
                now - self._start_time,  # runtime
                self.Util.get_memory_usage() / self.Util.MB_TO_BYTE,  # ram
                self.Util.get_cpu_usage(),  # cpu

                self._api_request.latest_run.strftime(DATETIME_FORMAT),  # api request latest
                self._db_insert.latest_run.strftime(DATETIME_FORMAT),  # db insert latest
                self._latest_run.strftime(DATETIME_FORMAT),  # status report latest

                unique_request_list["queued"][2],  # queued guild stat
                unique_request_list["eligible"][2],  # eligible guild stat
                unique_request_list["running"][2],  # running guild stat

                unique_request_list["queued"][1],  # queued online players
                unique_request_list["eligible"][1],  # eligible online players
                unique_request_list["running"][1],  # running online players

                unique_request_list["queued"][0],  # queued player stat
                unique_request_list["eligible"][0],  # eligible player stat
                unique_request_list["running"][0],  # running player stat

                self._api.ratelimit.remaining,  # ratelimit
                len(self._db_insert.response_handler.online_players),  # online player
                len(self._db_insert.response_handler.online_guilds),  # online guild

                avg_guild_req_duration,  # avg guild req duration
                avg_onlineplayers_req_duration,  # avg onlineplayers req duration
                avg_player_req_duration,  # avg player req duration

                recent_guild_reqs,  # n amount of recent guild reqs
                recent_onlineplayers_reqs,  # n amount of recent onlineplayers reqs
                recent_player_reqs,  # n amount of recent player reqs,
                recent_all_reqs,  # n amount of recent all reqs

                self.Util.get_os_info(),  # os
                self.Util.get_os_uptime()  # uptime
        )
        return msg

    class Util:
        KB_TO_BYTE = 1024
        MB_TO_BYTE = 1024 * KB_TO_BYTE

        @staticmethod
        def get_memory_usage() -> int:
            """Get the memory usage of the current process in bytes.

            Returns:
                int: Memory usage in bytes.
            """
            process = psutil.Process()
            memory_info = process.memory_info()
            return memory_info.rss

        @staticmethod
        def get_cpu_usage() -> float:
            process = psutil.Process()
            return process.cpu_percent()

        @staticmethod
        def get_os_info() -> str:
            return f"{platform.system()} {platform.release()} {platform.version()}"

        @staticmethod
        def get_os_uptime() -> timedelta:
            uptime_seconds = psutil.boot_time()
            uptime_datetime = datetime.fromtimestamp(uptime_seconds)
            return datetime.now() - uptime_datetime

    @property
    def first_delay(self) -> float:
        return 5.0

    @property
    def interval(self) -> float:
        return 5.0

    @property
    def latest_run(self) -> datetime:
        return self._latest_run

    @property
    def name(self) -> str:
        return self.__class__.__name__


# https://tree.nathanfriend.io/
# - faz-db Stats
#  - Runtime: 
#  - RAM: 
# - Tasks
#  - ApiRequest Latest: 
#  - DbInsert Latest: 
#  - StatusReport Latest: 
#  - RequestList
#   - Queued
#    - PlayerStat: 
#    - OnlinePlayers: 
#    - GuildStat: 
#   - Eligible
#    - PlayerStat: 
#    - OnlinePlayers: 
#    - GuildStat: 
#   - Running
#    - PlayerStat: 
#    - OnlinePlayers: 
#    - GuildStat: 
 
# - Db Stats
#   - Size: 
  
# - Api Stats
#  - Ratelimit: 
#  - Online Player: 
#  - Online Guild: 
 
# - System Stats
#  - OS: 
#  - Uptime: 
