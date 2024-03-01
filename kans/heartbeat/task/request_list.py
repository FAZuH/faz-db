from __future__ import annotations
from datetime import datetime
from threading import Lock
from typing import TYPE_CHECKING, Any, Coroutine, Generator

if TYPE_CHECKING:
    from kans import Api
    from kans.api.wynn.response import AbstractWynnResponse


class RequestList:

    def __init__(self) -> None:
        self._api: Api  # TODO: inject dependency into constructor
        self._list: list[RequestList.RequestItem] = []
        self._lock: Lock = Lock()

    def dequeue(self, amount: int) -> list[Coroutine[AbstractWynnResponse[Any], Any, Any]]:
        now = datetime.now().timestamp()

        ret = []
        with self._lock:
            for _ in range(amount):
                if len(self._list) < 1:
                    break

                item: RequestList.RequestItem = min(self._list)
                if item.is_eligible(now):
                    self._list.remove(item)
                    ret.append(item.coro)
                else:
                    # Stop yielding because the rest of the list is not eligible
                    break
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

        def __eq__(self, other: object | RequestList.RequestItem) -> bool:
            if isinstance(other, RequestList.RequestItem):
                return (
                        (self.coro.cr_frame.f_locals == other.coro.cr_frame.f_locals) and
                        (self.coro.__qualname__ == other.coro.__qualname__)
                )
            return False

        def __lt__(self, other: RequestList.RequestItem) -> bool:
            """For min() function."""
            # NOTE: priority check is used to prioritize online uuids request
            if self.is_eligible() is False:
                # NOTE: items not eligible obviously shouldn't be included in the min() result
                return False

            # NOTE: If the priority value is different, the item with the higher priority is chosen.
            # Else, the item with the lower request timestamp is chosen.
            if self.priority != other.priority:
                return self.priority > other.priority
            else:
                return self.req_ts < other.req_ts

        @property
        def req_ts(self) -> float:
            return self._req_ts

        @property
        def coro(self) -> Coroutine[AbstractWynnResponse[Any], Any, Any]:
            return self._coro

        @property
        def priority(self) -> int:
            return self._priority
