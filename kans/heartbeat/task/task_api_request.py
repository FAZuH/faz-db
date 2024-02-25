from __future__ import annotations
import asyncio
from datetime import datetime as dt
from typing import TYPE_CHECKING, Any

from . import Task

if TYPE_CHECKING:
    from loguru import Logger
    from . import RequestList, ResponseList
    from kans import Api
    from kans.api.wynn.response import AbstractWynnResponse


class TaskApiRequest(Task):
    """implements `TaskBase`"""

    def __init__(self, logger: Logger, api: Api, request_list: RequestList, response_list: ResponseList) -> None:
        self._logger = logger
        self._api: Api = api
        self._request_list = request_list
        self._response_list = response_list

        self._concurrent_request = 20  # NOTE: request/min need to stay below 180, else running requests will increase without bound
        self._event_loop = asyncio.new_event_loop()
        self._latest_run = dt.now()
        self._running_requests: list[asyncio.Task[AbstractWynnResponse[Any]]] = []

    def setup(self) -> None:
        self._logger.debug(f"Setting up {self.name}")
        self._event_loop.run_until_complete(self._api.start())

    def teardown(self) -> None:
        self._logger.debug(f"Tearing down {self.name}")
        self._event_loop.run_until_complete(self._api.close())

    def run(self) -> None:
        self._event_loop.run_until_complete(self._run())
        self._latest_run = dt.now()

    async def _run(self) -> None:
        await self._check_api_session()

        if self._api.ratelimit.remaining > 0:
            for req in self._request_list.get(self._concurrent_request):
                self._running_requests.append(self._event_loop.create_task(req))

        ok_results: list[AbstractWynnResponse[Any]] = []
        tasks_to_remove = []
        for req in self._running_requests:
            if not req.done():
                continue

            tasks_to_remove.append(req)
            if req.exception():
                self._logger.error(f"Error fetching from Wynn API: {req.exception()}")
                # HACK: prevents WynnApiFetcher stopping when get_online_uuids is not requeued
                if req.get_coro().__qualname__ == self._api.player.get_online_uuids.__qualname__:
                    self._request_list.put(0, self._api.player.get_online_uuids)
            else:
                ok_results.append(req.result())

        for req in tasks_to_remove:
            self._running_requests.remove(req)

        self._logger.debug(f"{len(ok_results)} responses from API")
        self._response_list.put(ok_results)

    async def _check_api_session(self) -> None:
        if not self._api.request.is_open():
            self._logger.warning("HTTP session is closed. Reopening...")
            await self._api.start()

    @property
    def running_requests(self) -> list[asyncio.Task[AbstractWynnResponse[Any]]]:
        return self._running_requests

    @property
    def first_delay(self) -> float:
        return 2.0

    @property
    def interval(self) -> float:
        return 5.0

    @property
    def latest_run(self) -> dt:
        return self._latest_run

    @property
    def name(self) -> str:
        return self.__class__.__name__
