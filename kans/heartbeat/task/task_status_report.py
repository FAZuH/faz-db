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
                message = await hook.fetch_message(self._message_id)
                await message.edit(content=report)

    _DEFAULT_MSG = \
            "```yaml"\
            "\n."\
            "\n├── Kans Stats/"\
            "\n│   ├── Runtime: {}"\
            "\n│   ├── RAM: {}"\
            "\n│   └── Tasks/"\
            "\n│       ├── Api Request/"\
            "\n│       │   ├── Latest: {}"\
            "\n│       │   ├── Queued Request: {}"\
            "\n│       │   ├── Gettable Request: {}"\
            "\n│       │   └── Running Request: {}"\
            "\n│       ├── Db Insert/"\
            "\n│       │   └── Latest: {}"\
            "\n│       └── Status Report/"\
            "\n│           └── Latest: {}"\
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

    async def _get_report(self) -> str:
        now = dt.now()
        msg = self._DEFAULT_MSG.format(
                now - self._start_time,  # runtime
                self.Util.get_memory_usage() / self.Util.MB_TO_BYTE,  # ram

                now - self._api_request.latest_run,  # api request latest
                self._request_list.length,  # queued request
                self._request_list.count_gettable(),  # gettable request
                len(self._api_request.running_requests),  # running request

                now - self._db_insert.latest_run,  # db insert latest

                now - self._latest_run,  # status report latest

                f"{await self._db.total_size() / self.Util.MB_TO_BYTE} MB",  # TODO: get db size

                self._api.ratelimit.remaining,  # ratelimit
                len(self._db_insert.online_players_manager.prev_online_uuids),  # online player
                len(self._db_insert.online_guilds_manager.prev_online_guilds),  # online guild

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
        return 15.0

    @property
    def interval(self) -> float:
        return 15.0

    @property
    def latest_run(self) -> dt:
        return self._latest_run

    @property
    def name(self) -> str:
        return self.__class__.__name__


# .
# ├── Kans Stats/
# │   ├── Runtime: 
# │   ├── RAM: 
# │   └── Tasks/
# │       ├── Api Request/
# │       │   ├── Latest: 
# │       │   ├── Queued Request: 
# │       │   ├── Gettable Request: 
# │       │   └── Running Request: 
# │       ├── Db Insert/
# │       │   └── Latest: 
# │       └── Status Report/
# │           └── Latest: 
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
#  - Tasks
#    - Api Request
#     - Latest: 
#     - Queued Request: 
#     - Gettable Request: 
#     - Running Request: 
#   - Db Insert
#    - Latest: 
#   - Status Report
#    - Latest: 
 
# - Db Stats
#   - Size: 
  
# - Api Stats
#  - Ratelimit: 
#  - Online Player: 
#  - Online Guild: 
 
# - System Stats
#  - OS: 
#  - Uptime: 
