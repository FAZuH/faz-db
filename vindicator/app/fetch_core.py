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
    from vindicator import AbstractFetch, AbstractRequest


class FetchCore:
    """Main class that manages request loop for all Fetch objects"""

    def __init__(self) -> None:
        # Internal Fetcher State
        self._concurrent_request: int = 36
        self._running: bool = False
        self._running_request: list[AbstractRequest[Any]] = []
        self._task: None | asyncio.Task[None] = None
        # Other Processes
        self._queue: FetchQueue = FetchQueue()
        self._wynnapi: WynnApi = WynnApi()
        self._wynnrepo: WynnDataRepository = WynnDataRepository()
        # Fetchers
        self._fetch_guild: AbstractFetch[Any] = FetchGuild(self)
        self._fetch_online: AbstractFetch[Any] = FetchOnline(self)
        self._fetch_player: AbstractFetch[Any] = FetchPlayer(self)

    async def start(self) -> None:
        while True:
            await self._do_requests()
            if not self._running:
                logger.debug("Running loop")
                self._running = True
                async with asyncio.TaskGroup() as tg:
                    t1 = tg.create_task(self._fetch_online.run())
                    t2 = tg.create_task(self._fetch_player.run())
                    t3 = tg.create_task(self._fetch_guild.run())
                res = [t1, t2, t3]
                for t in res:
                    if t.done() and t.exception():
                        await t
                self._running = False
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
