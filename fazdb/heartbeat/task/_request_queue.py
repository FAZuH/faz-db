from __future__ import annotations
from datetime import datetime
from threading import Lock
from typing import Any, Coroutine, Generator, TYPE_CHECKING

from . import RequestItem

if TYPE_CHECKING:
    from fazdb.api.wynn.response import AbstractWynnResponse


type WynnRespCoro = Coroutine[AbstractWynnResponse[Any], Any, Any]


class RequestQueue:

    def __init__(self) -> None:
        # self._api: Api  # TODO: inject dependency into constructor
        self._list: list[RequestItem] = []
        self._lock: Lock = Lock()

    def dequeue(self, amount: int) -> list[WynnRespCoro]:
        now = datetime.now().timestamp()
        ret: list[WynnRespCoro] = []
        with self._lock:
            for _ in range(amount):
                item = self.__dequeue_one(now)
                if item is None:
                    # Stop yielding because the rest of the list is not eligible
                    break
                ret.append(item.coro)
        return ret

    def enqueue(self, request_ts: float, coro: WynnRespCoro, priority: int = 100) -> None:
        with self._lock:
            item = RequestItem(coro, priority, request_ts)
            if item not in self._list:
                self._list.append(item)

    def iter(self) -> Generator[RequestItem, Any, None]:
        with self._lock:
            yield from self._list

    def __dequeue_one(self, ts: None | float) -> None | RequestItem:
        if len(self._list) < 1:
            return None

        item = min(self._list)
        if item.is_eligible(ts):
            self._list.remove(item)
            return item
