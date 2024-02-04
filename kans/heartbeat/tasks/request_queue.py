from __future__ import annotations
from datetime import datetime as dt
from threading import Lock
from typing import Any, Awaitable, Callable, Generator


class _RequestItem:

    def __init__(self, req_time: float, coro_f: Callable[..., Awaitable[Any]], requestarg: str) -> None:
        self._req_time = req_time
        self._coro_f = coro_f
        self._requestarg = requestarg

    def __eq__(self, other: object) -> bool:
        if isinstance(other, _RequestItem):
            return self.requestarg == other.requestarg
        elif isinstance(other, str):
            return self.requestarg == other
        return False

    def __lt__(self, other: _RequestItem) -> bool:
        """For min() function."""
        return self.req_time < other.req_time

    @property
    def req_time(self) -> float:
        return self._req_time

    @property
    def coro_f(self) -> Callable[..., Awaitable[Any]]:
        return self._coro_f

    @property
    def requestarg(self) -> str:
        return self._requestarg


class RequestQueue:

    def __init__(self) -> None:
        self._queue: list[_RequestItem] = []
        self._lock: Lock = Lock()

    def getmany(self, amount: int) -> Generator[_RequestItem, Any, None]:
        now: float = dt.now().timestamp()
        with self._lock:
            for _ in range(amount):
                if len(self._queue) == 0:
                    return
                min_item: _RequestItem = min(self._queue)
                if min_item.req_time < now:
                    self._queue.remove(min_item)
                    yield min_item
                else:
                    return

    def put(self, schedule_time: float, coro_f: Callable[..., Awaitable[Any]], requestarg: str = '') -> None:
        with self._lock:
            if requestarg in self._queue:  # type: ignore
                return
            self._queue.append(_RequestItem(schedule_time, coro_f, requestarg))
