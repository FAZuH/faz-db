from __future__ import annotations
import asyncio
from datetime import datetime
from typing import Any, TYPE_CHECKING

from loguru import logger

from . import Task

if TYPE_CHECKING:
    from . import RequestQueue, ResponseQueue
    from fazdb import Api
    from fazdb.api.wynn.response import AbstractWynnResponse


class TaskApiRequest(Task):
    """implements `TaskBase`"""

    _CONCURRENT_REQUESTS = 15

    def __init__(self, api: Api, request_queue: RequestQueue, response_queue: ResponseQueue) -> None:
        self._api = api
        self._request_queue = request_queue
        self._response_queue = response_queue

        self._event_loop = asyncio.new_event_loop()
        self._latest_run = datetime.now()
        self._running_requests: list[asyncio.Task[AbstractWynnResponse[Any]]] = []

    # override
    def setup(self) -> None:
        self._event_loop.run_until_complete(self._api.start())

    # override
    def teardown(self) -> None:
        self._event_loop.run_until_complete(self._api.close())
        for req in self._running_requests:
            req.cancel()

    # override
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
                for req in self._request_queue.dequeue(self._CONCURRENT_REQUESTS - running_req_amount)
            )

    def _check_responses(self) -> None:
        ok_results: list[AbstractWynnResponse[Any]] = []
        # NOTE: remove tasks separately to avoid size changes during iteration
        tasks_to_remove = []
        for task in self._running_requests:
            if not task.done():
                continue

            tasks_to_remove.append(task)

            exc = task.exception()
            if exc is not None:
                # HACK: prevents WynnApiFetcher stopping when get_online_uuids is not requeued
                if task.get_coro().__qualname__ == self._api.player.get_online_uuids.__qualname__:
                    self._request_queue.enqueue(0, self._api.player.get_online_uuids(), priority=999)

                with logger.catch(level="ERROR"):
                    raise exc
            else:
                # get_online_uuids will be requeued when the response is computed
                ok_results.append(task.result())

        for task in tasks_to_remove:
            self._running_requests.remove(task)

        if ok_results:
            logger.info(f"{len(ok_results)} responses from API")
            self._response_queue.put(ok_results)

    @property
    def running_requests(self) -> list[asyncio.Task[AbstractWynnResponse[Any]]]:
        return self._running_requests

    # override
    @property
    def first_delay(self) -> float:
        return 2.0

    # override
    @property
    def interval(self) -> float:
        return 1.0

    # override
    @property
    def latest_run(self) -> datetime:
        return self._latest_run

    # override
    @property
    def name(self) -> str:
        return self.__class__.__name__
