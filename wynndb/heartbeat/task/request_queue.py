from __future__ import annotations
from datetime import datetime
from threading import Lock
from typing import TYPE_CHECKING, Any, Coroutine, Generator

if TYPE_CHECKING:
    from wynndb.api.wynn.response import AbstractWynnResponse


class RequestQueue:

    def __init__(self) -> None:
        # self._api: Api  # TODO: inject dependency into constructor
        self._list: list[RequestQueue.RequestItem] = []
        self._lock: Lock = Lock()

    def dequeue(self, amount: int) -> list[Coroutine[AbstractWynnResponse[Any], Any, Any]]:
        now = datetime.now().timestamp()

        ret: list[Coroutine[AbstractWynnResponse[Any], Any, Any]] = []
        with self._lock:
            for _ in range(amount):
                item = self._dequeue_one(now)
                if item is None:
                    # Stop yielding because the rest of the list is not eligible
                    break
                ret.append(item.coro)
        return ret

    def enqueue(
        self,
        request_ts: float,
        coro: Coroutine[AbstractWynnResponse[Any], Any, Any],
        priority: int = 100
    ) -> None:
        with self._lock:
            item = self.RequestItem(coro, priority, request_ts)
            if item not in self._list:
                self._list.append(item)

    def iter(self) -> Generator[RequestItem, Any, None]:
        with self._lock:
            yield from self._list

    def _dequeue_one(self, ts: None | float) -> None | RequestQueue.RequestItem:
        if len(self._list) < 1:
            return None

        item = min(self._list)
        if item.is_eligible(ts):
            self._list.remove(item)
            return item


    class RequestItem:

        def __init__(
            self,
            coro: Coroutine[AbstractWynnResponse[Any], Any, Any],
            priority: int,
            req_ts: float,
        ) -> None:
            self._req_ts = req_ts
            self._coro = coro
            self._priority = priority

        def is_eligible(self, timestamp: None | float = None) -> bool:
            timestamp = timestamp or datetime.now().timestamp()
            return self.req_ts < timestamp

        def __eq__(self, other: object | RequestQueue.RequestItem) -> bool:
            if isinstance(other, RequestQueue.RequestItem):
                return (
                        (self.coro.cr_frame.f_locals == other.coro.cr_frame.f_locals) and
                        (self.coro.__qualname__ == other.coro.__qualname__)
                )
            return False

        def __lt__(self, other: RequestQueue.RequestItem) -> bool:
            """For min() function.
            Return true to get favored more in min() function."""
            if self.is_eligible() is False:
                # items not eligible (expired endpoint) obviously shouldn't be favored in min()
                return False

            if self.priority != other.priority:
                # Higher priority is favored
                return self.priority > other.priority
            else:
                # Favor requests that has expired longer
                return self.req_ts < other.req_ts

        @property
        def req_ts(self) -> float:
            """Timestamp for when the cache of the resource will expire."""
            return self._req_ts

        @property
        def coro(self) -> Coroutine[AbstractWynnResponse[Any], Any, Any]:
            return self._coro

        @property
        def priority(self) -> int:
            return self._priority
