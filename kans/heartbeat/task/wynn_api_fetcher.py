from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING, Any

from . import Task

if TYPE_CHECKING:
    from loguru import Logger
    from . import RequestList, ResponseList
    from kans.api import Api
    from kans.api.wynn.response import AbstractWynnResponse


class WynnApiFetcher(Task):
    """implements `TaskBase`"""

    def __init__(self, logger: Logger, api: Api, request_list: RequestList, response_list: ResponseList) -> None:
        self._logger = logger
        self._request_list = request_list
        self._response_list = response_list
        self._api = api

        self._concurrent_request = 14  # NOTE: request/min need to stay below 180, else running requests will increase without bound
        self._event_loop = asyncio.new_event_loop()
        self._running_requests: list[asyncio.Task[AbstractWynnResponse[Any]]] = []

    def setup(self) -> None:
        self._logger.debug(f"Setting up {self.name}")
        self._event_loop.run_until_complete(self._api.start())

    def teardown(self) -> None:
        self._logger.debug(f"Tearing down {self.name}")
        self._event_loop.run_until_complete(self._api.close())

    def run(self) -> None:
        self._event_loop.run_until_complete(self._run())
        self._logger.debug(f"{self._request_list.length} in {self._request_list.__class__.__name__}")
        self._logger.debug(f"{len(self._running_requests)} running")
        self._logger.debug(f"{self._api.ratelimit.remaining} remaining ratelimit")

    async def _run(self) -> None:
        if self._api.ratelimit.remaining > 0:
            for req in self._request_list.get(self._concurrent_request):
                self._running_requests.append(self._event_loop.create_task(req))

        ok_results: list[AbstractWynnResponse[Any]] = []
        for req in self._running_requests:
            if not req.done():
                continue
            if req.exception():
                self._running_requests.remove(req)
                self._logger.error(f"Error fetching from Wynn API: {req.exception()}")
                continue

            ok_results.append(req.result())
            self._running_requests.remove(req)

        self._logger.debug(f"{len(ok_results)} responses from API")
        self._response_list.put(ok_results)

    @property
    def first_delay(self) -> float:
        return 1.0

    @property
    def interval(self) -> float:
        return 5.0

    @property
    def name(self) -> str:
        return self.__class__.__name__
