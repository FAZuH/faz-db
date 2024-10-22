from __future__ import annotations
import asyncio
from datetime import datetime
from typing import Any, TYPE_CHECKING

from loguru import logger

from . import ITask

if TYPE_CHECKING:
    from .request_queue import RequestQueue
    from .response_queue import ResponseQueue
    from fazdb.api import WynnApi, BaseResponse
    type BaseResponse_ = BaseResponse[Any, Any]


class TaskApiRequest(ITask):
    """implements `TaskBase`"""

    _CONCURRENT_REQUESTS = 15

    def __init__(self, api: WynnApi, request_queue: RequestQueue, response_queue: ResponseQueue) -> None:
        self._api = api
        self._request_list = request_queue
        self._response_list = response_queue

        self._event_loop = asyncio.new_event_loop()
        self._latest_run = datetime.now()
        self._running_requests: list[asyncio.Task[BaseResponse_]] = []

    def setup(self) -> None:
        logger.debug(f"Setting up {self.name}")
        self._event_loop.run_until_complete(self._api.start())

    def teardown(self) -> None:
        logger.debug(f"Tearing down {self.name}")
        self._event_loop.run_until_complete(self._api.close())
        for req in self._running_requests:
            req.cancel()

    def run(self) -> None:
        with logger.catch(level="ERROR"):
            self._event_loop.run_until_complete(self._run())
        self._latest_run = datetime.now()

    async def _run(self) -> None:
        await self._check_api_session()
        self._start_requests()
        self._check_responses()

    async def _check_api_session(self) -> None:
        if not self._api.request.is_open():
            logger.warning("HTTP session is closed. Reopening...")
            await self._api.start()

    def _start_requests(self) -> None:
        # NOTE: This prevents being ratelimited,
        # since requests won't be finishing when the client is ratelimited
        running_req_amount = len(self._running_requests)
        if running_req_amount < self._CONCURRENT_REQUESTS:
            self._running_requests.extend(
                self._event_loop.create_task(req)
                # fill the event loop with eligible requests once there's slots open
                for req in self._request_list.dequeue(self._CONCURRENT_REQUESTS - running_req_amount)
            )

    def _check_responses(self) -> None:
        ok_results: list[BaseResponse_] = []
        tasks_to_remove = []
        for task in self._running_requests:
            if not task.done():
                continue

            tasks_to_remove.append(task)
            exc = task.exception()
            if exc is not None:
                if task.get_coro().__qualname__ == self._api.player.get_online_uuids.__qualname__:
                    self._request_list.enqueue(0, self._api.player.get_online_uuids())

                # HACK: prevents WynnApiFetcher stopping when get_online_uuids is not requeued
                with logger.catch():
                    raise exc
            else:
                # get_online_uuids will be requeued when the response is computed
                ok_results.append(task.result())

        for task in tasks_to_remove:
            self._running_requests.remove(task)

        if len(ok_results) > 0:
            logger.debug(f"{len(ok_results)} responses from API")
            self._response_list.put(ok_results)

    @property
    def first_delay(self) -> float:
        return 2.0

    @property
    def interval(self) -> float:
        return 1.0

    @property
    def latest_run(self) -> datetime:
        return self._latest_run

    @property
    def name(self) -> str:
        return self.__class__.__name__
