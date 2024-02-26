from __future__ import annotations
from datetime import datetime as dt
from threading import Lock
from typing import TYPE_CHECKING, Any, Coroutine, Generator

if TYPE_CHECKING:
    from kans.api.wynn.response import AbstractWynnResponse


class _RequestItem:

    def __init__(
        self,
        coro: Coroutine[AbstractWynnResponse[Any], Any, Any],
        priority: int,
        req_ts: float,
    ) -> None:
        self._req_ts = req_ts
        self._coro = coro
        self._priority = priority

    def is_elligible(self, timestamp: None | float = None) -> bool:
        return self.req_ts < (timestamp or dt.now().timestamp())

    def __eq__(self, other: object | _RequestItem) -> bool:
        if isinstance(other, _RequestItem):
            return (
                (self.coro.cr_frame.f_locals == other.coro.cr_frame.f_locals) and
                (self.coro.__qualname__ is other.coro.__qualname__)
            )
        return False

    def __lt__(self, other: _RequestItem) -> bool:
        """For min() function."""
        # NOTE: priority check is used to prioritize online uuids request
        return (self.req_ts < other.req_ts) or (self.priority > other.priority)

    @property
    def req_ts(self) -> float:
        return self._req_ts

    @property
    def coro(self) -> Coroutine[AbstractWynnResponse[Any], Any, Any]:
        return self._coro

    @property
    def priority(self) -> int:
        return self._priority


class RequestList:

    def __init__(self) -> None:
        self._list: list[_RequestItem] = []
        self._lock: Lock = Lock()

    def get(self, amount: int) -> Generator[Coroutine[AbstractWynnResponse[Any], Any, Any], Any, None]:
        now: float = dt.now().timestamp()

        with self._lock:
            for _ in range(amount):
                if len(self._list) < 1:
                    return

                item: _RequestItem = min(self._list)
                if item.is_elligible(now):
                    self._list.remove(item)
                    yield item.coro
                else:
                    # Stop yielding because the rest of the list is not eligible
                    return

    def put(
        self,
        request_ts: float,
        coro: Coroutine[AbstractWynnResponse[Any], Any, Any],
        priority: int = 100
    ) -> None:
        with self._lock:
            item = _RequestItem(coro, priority, request_ts)
            if item not in self._list:
                self._list.append(item)

    def iter(self) -> Generator[_RequestItem, Any, None]:
        with self._lock:
            for item in self._list:
                yield item
