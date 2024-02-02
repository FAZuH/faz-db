from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING, Any, Awaitable

from vindicator import (
    logger,
    FetchGuild,
    FetchOnline,
    FetchPlayer,
    RequestLevel,
    FetchQueue,
    WynnApi,
    WynnDataRepository
)

if TYPE_CHECKING:
    from vindicator import Fetch, Request


class FetchCore:
    """Main class that manages request loop for all Fetch objects"""

    def __init__(self) -> None:
        # Internal Fetcher State
        self._concurrent_request: int = 25
        self._running: bool = False
        self._running_request: list[Request[Any]] = []
        self._task: None | asyncio.Task[None] = None
        # Other Processes
        self._queue: FetchQueue = FetchQueue()
        self._wynnapi: WynnApi = WynnApi()
        self._wynnrepo: WynnDataRepository = WynnDataRepository()
        # Fetchers
        self._fetch_guild: Fetch[Any] = FetchGuild(self)
        self._fetch_online: Fetch[Any] = FetchOnline(self)
        self._fetch_player: Fetch[Any] = FetchPlayer(self)

    async def start(self) -> None:
        self._running = True
        logger.debug("Running loop")
        while True:
            async with asyncio.TaskGroup() as tg:
                tg.create_task(self._do_requests())
                tg.create_task(self._fetch_online.run())
                tg.create_task(self._fetch_player.run())
                tg.create_task(self._fetch_guild.run())
            await asyncio.sleep(5)

    def stop(self) -> None:
        self._running = False

    def cancel(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()

    async def _do_requests(self) -> None:
        if len(self._running_request) != 0:
            return

        self._running_request = self._queue.get(self._concurrent_request)
        coros: list[Awaitable[None]] = [req.run() for req in self._running_request]

        async with self._wynnapi:
            # TODO: catch and log exceptions
            await asyncio.gather(*coros, return_exceptions=True)
            for req in self._running_request:
                if not req.done:
                    continue
                match req.level:
                    case RequestLevel.GUILD:
                        self._fetch_guild.append_request(req)
                    case RequestLevel.ONLINE:
                        self._fetch_online.append_request(req)
                    case RequestLevel.PLAYER:
                        self._fetch_player.append_request(req)
            self._running_request.clear()

    @property
    def queue(self) -> FetchQueue:
        return self._queue

    @property
    def wynnapi(self) -> WynnApi:
        return self._wynnapi

    @property
    def wynnrepo(self) -> WynnDataRepository:
        return self._wynnrepo
