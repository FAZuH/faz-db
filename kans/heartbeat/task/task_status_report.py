from __future__ import annotations
import asyncio
from datetime import datetime as dt
import platform
import psutil
from typing import TYPE_CHECKING

from aiohttp import ClientSession
import discord

from . import Task

if TYPE_CHECKING:
    from datetime import timedelta
    from loguru import Logger
    from . import RequestList, TaskApiRequest, TaskDbInsert
    from kans import Api, ConfigT, Database


class TaskStatusReport(Task):

    def __init__(
        self,
        config: ConfigT,
        logger: Logger,
        api: Api,
        api_request: TaskApiRequest,
        db: Database,
        db_insert: TaskDbInsert,
        request_list: RequestList
    ) -> None:
        self._logger = logger
        self._api = api
        self._api_request = api_request
        self._db = db
        self._db_insert = db_insert
        self._request_list = request_list

        self._event_loop = asyncio.new_event_loop()
        self._latest_run = self._start_time = dt.now()
        self._message_id: None | int = None
        self._url = config["STATUS_REPORT_WEBHOOK"]

    def setup(self) -> None:
        self._event_loop.run_until_complete(self.async_setup())

    def teardown(self) -> None: ...

    def run(self) -> None:
        self._event_loop.run_until_complete(self._run())
        self._latest_run = dt.now()

    async def async_setup(self):
        async with ClientSession() as s:
            hook = discord.Webhook.from_url(self._url, session=s)

            await hook.edit(
                    name="Kans Information",
                    # TODO: set avatar
            )
            await hook.send("Started Kans.")

    async def _run(self) -> None:
        await self._send()

    async def _send(self) -> None:
        async with ClientSession() as s:
            hook = discord.Webhook.from_url(self._url, session=s)
            report = await self._get_report()

            if self._message_id is None:
                message = await hook.send(content=report, wait=True)
                self._message_id = message.id
            else:
                try:
                    message = await hook.fetch_message(self._message_id)
                except discord.DiscordException:
                    self._logger.exception("Failed to fetch message.")
                    self._message_id = None
                    return

                await message.edit(content=report)

    _DEFAULT_MSG = \
            "```yaml"\
            "\n."\
            "\n├── Kans Stats/"\
            "\n│   ├── Runtime: {}"\
            "\n│   └── RAM: {}"\
            "\n├── Tasks/"\
            "\n│   ├── ApiRequest Latest: {}"\
            "\n│   ├── DbInsert Latest: {}"\
            "\n│   ├── StatusReport Latest: {}"\
            "\n│   └── RequestList/"\
            "\n│       ├── Queued/"\
            "\n│       │   ├── PlayerStat: {}"\
            "\n│       │   ├── OnlinePlayers: {}"\
            "\n│       │   └── GuildStat: {}"\
            "\n│       ├── Eligible/"\
            "\n│       │   ├── PlayerStat: {}"\
            "\n│       │   ├── OnlinePlayers: {}"\
            "\n│       │   └── GuildStat: {}"\
            "\n│       └── Running/"\
            "\n│           ├── PlayerStat: {}"\
            "\n│           ├── OnlinePlayers: {}"\
            "\n│           └── GuildStat: {}"\
            "\n├── Db Stats/"\
            "\n│   └── Size: {}"\
            "\n├── Api Stats/"\
            "\n│   ├── Ratelimit: {}"\
            "\n│   ├── Online Player: {}"\
            "\n│   └── Online Guild: {}"\
            "\n└── System Stats/"\
            "\n    ├── OS: {}"\
            "\n    └── Uptime: {}"\
            "\n```"

    # TODO: unique count of request types on RequestList
    # TODO: average requests per minute
    # TODO: clean code
    async def _get_report(self) -> str:
        now = dt.now()
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
            if req.is_elligible(now_ts):
                unique_request_list["eligible"][index] += 1

        for req in self._api_request.running_requests.copy():
            coro = req.get_coro()
            index = match_qualname.get(coro.__qualname__, 3)
            unique_request_list["running"][index] += 1

        msg = self._DEFAULT_MSG.format(
                now - self._start_time,  # runtime
                self.Util.get_memory_usage() / self.Util.MB_TO_BYTE,  # ram

                self._api_request.latest_run,  # api request latest
                self._db_insert.latest_run,  # db insert latest
                self._latest_run,  # status report latest

                unique_request_list["queued"][0],  # queued player stat
                unique_request_list["queued"][1],  # queued online players
                unique_request_list["queued"][2],  # queued guild stat
                unique_request_list["eligible"][0],  # eligible player stat
                unique_request_list["eligible"][1],  # eligible online players
                unique_request_list["eligible"][2],  # eligible guild stat
                unique_request_list["running"][0],  # running player stat
                unique_request_list["running"][1],  # running online players
                unique_request_list["running"][2],  # running guild stat

                f"{await self._db.total_size() / self.Util.MB_TO_BYTE} MB",  # db size

                self._api.ratelimit.remaining,  # ratelimit
                len(self._db_insert.players_manager.online_uuids),  # online player
                len(self._db_insert.guilds_manager.online_guilds),  # online guild

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
        def get_os_info() -> str:
            return f"{platform.system()} {platform.release()} {platform.version()}"

        @staticmethod
        def get_os_uptime() -> timedelta:
            uptime_seconds = psutil.boot_time()
            uptime_datetime = dt.fromtimestamp(uptime_seconds)
            return dt.now() - uptime_datetime

    @property
    def first_delay(self) -> float:
        return 5.0

    @property
    def interval(self) -> float:
        return 5.0

    @property
    def latest_run(self) -> dt:
        return self._latest_run

    @property
    def name(self) -> str:
        return self.__class__.__name__


# .
# ├── Kans Stats/
# │   ├── Runtime: 
# │   └── RAM: 
# ├── Tasks/
# │   ├── ApiRequest Latest: 
# │   ├── DbInsert Latest: 
# │   ├── StatusReport Latest: 
# │   └── RequestList/
# │       ├── Queued/
# │       │   ├── PlayerStat: 
# │       │   ├── OnlinePlayers: 
# │       │   └── GuildStat: 
# │       ├── Eligible/
# │       │   ├── PlayerStat: 
# │       │   ├── OnlinePlayers: 
# │       │   └── GuildStat: 
# │       └── Running/
# │           ├── PlayerStat: 
# │           ├── OnlinePlayers: 
# │           └── GuildStat: 
# ├── Db Stats/
# │   └── Size: 
# ├── Api Stats/
# │   ├── Ratelimit: 
# │   ├── Online Player: 
# │   └── Online Guild: 
# └── System Stats/
#     ├── OS: 
#     └── Uptime: 

# https://tree.nathanfriend.io/
# - Kans Stats
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
