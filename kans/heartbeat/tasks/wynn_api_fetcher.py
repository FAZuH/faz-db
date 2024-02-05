from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING

from kans import TaskBase, WynnResponse

if TYPE_CHECKING:
    from loguru import Logger
    from kans import RequestQueue, WynnApi, WynnDataLogger


class WynnApiFetcher(TaskBase):
    """implements `TaskBase`"""

    def __init__(
        self,
        logger: Logger,
        wynnapi: WynnApi,
        wynn_data_logger: WynnDataLogger,
        request_queue: RequestQueue,
    ) -> None:
        self._logger = logger
        self._request_queue = request_queue
        self._wynnapi = wynnapi
        self._wynn_data_logger = wynn_data_logger

        self._concurrent_request = 36
        self._event_loop = asyncio.new_event_loop()

    def run(self) -> None:
        self._event_loop.run_until_complete(self._run())

    async def _run(self) -> None:
        coros = tuple(
            item.coro_f(item.requestarg)
            for item in self._request_queue.getmany(self._concurrent_request)
        )
        async with self._wynnapi:
            resps = await asyncio.gather(*coros, return_exceptions=True)

        for resp in resps:
            if isinstance(resp, Exception):
                # TODO: Log exception
                pass
            elif isinstance(resp, WynnResponse):
                self._wynn_data_logger.put_response(resp)

    @property
    def first_delay(self) -> float:
        return 1.0

    @property
    def interval(self) -> float:
        return 5.0

    @property
    def name(self) -> str:
        return "WynnApiFetcher"
