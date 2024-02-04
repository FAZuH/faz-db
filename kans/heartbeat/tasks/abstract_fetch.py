from __future__ import annotations
from abc import ABC, abstractmethod
import asyncio
from threading import Lock
from typing import TYPE_CHECKING, Any, Generator, Generic, TypeVar

from kans import TaskBase

if TYPE_CHECKING:
    from kans import App, RequestQueue

T = TypeVar('T')


class AbstractFetch(TaskBase, Generic[T], ABC):
    def __init__(self, app: App, request_queue: RequestQueue) -> None:
        self._app = app
        self._request_queue = request_queue

        self._event_loop = asyncio.new_event_loop()
        self._response_lock = Lock()
        self._unprocessed_response = []

    def popall_unprocessed_response(self) -> Generator[T, Any, None]:
        with self._response_lock:
            while self._unprocessed_response:
                yield self._unprocessed_response.pop()

    def put_response(self, response: T) -> None:
        with self._response_lock:
            self._unprocessed_response.append(response)

    def run(self) -> None:
        self._event_loop.run_until_complete(self._run())

    @property
    def app(self) -> App:
        return self._app

    @property
    def request_queue(self) -> RequestQueue:
        return self._request_queue

    @abstractmethod
    async def _run(self) -> None: ...

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def first_delay(self) -> float: ...

    @property
    @abstractmethod
    def interval(self) -> float: ...
