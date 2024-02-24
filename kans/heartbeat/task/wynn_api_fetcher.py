from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING, Any

from kans import Task

if TYPE_CHECKING:
    from loguru import Logger
    from kans import Api, RequestList, ResponseList


class WynnApiFetcher(Task):
    """implements `TaskBase`"""

    def __init__(self, logger: Logger, wynnapi: Api, request_list: RequestList, response_list: ResponseList) -> None:
        self._logger = logger
        self._request_list = request_list
        self._response_list = response_list
        self._wynnapi = wynnapi

        self._concurrent_request = 25
        self._event_loop = asyncio.new_event_loop()

    def run(self) -> None:
        self._event_loop.run_until_complete(self._run())

    async def _run(self) -> None:
        coros = tuple(coro for coro in self._request_list.get(self._concurrent_request))

        async with self._wynnapi:
            results: list[Any | BaseException] = await asyncio.gather(*coros, return_exceptions=True)

        self._response_list.put(tuple(res for res in results if not isinstance(res, BaseException)))

    @property
    def first_delay(self) -> float:
        return 1.0

    @property
    def interval(self) -> float:
        return 5.0

    @property
    def name(self) -> str:
        return "WynnApiFetcher"
