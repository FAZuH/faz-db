from __future__ import annotations
from datetime import datetime as dt
from threading import Lock
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Generator

if TYPE_CHECKING:
    from kans.api.wynn.response import AbstractWynnResponse


class _RequestItem:

    def __init__(self, req_ts: float, afunc: Callable[..., Coroutine[AbstractWynnResponse[Any], Any, Any]], args: tuple[Any, ...] = tuple()) -> None:
        self._req_time = req_ts
        self._afunc = afunc
        self._args = args

    def __eq__(self, other: object | _RequestItem) -> bool:
        if isinstance(other, _RequestItem):
            return (self.args == other.args) and (self.afunc.__func__ is other.afunc.__func__)  # type: ignore
        return False

    def __lt__(self, other: _RequestItem) -> bool:
        """For min() function."""
        return self.req_ts < other.req_ts

    @property
    def req_ts(self) -> float:
        return self._req_time

    @property
    def afunc(self) -> Callable[..., Coroutine[AbstractWynnResponse[Any], Any, Any]]:
        return self._afunc

    @property
    def args(self) -> tuple[Any, ...]:
        return self._args


class RequestList:

    def __init__(self) -> None:
        self._list: list[_RequestItem] = []
        self._lock: Lock = Lock()

    def get(self, amount: int) -> Generator[Coroutine[AbstractWynnResponse[Any], Any, Any], Any, None]:
        now: float = dt.now().timestamp()

        with self._lock:
            for _ in range(amount):
                if len(self._list) == 0 :
                    return

                min_item: _RequestItem = min(self._list)
                if min_item.req_ts < now:
                    self._list.remove(min_item)
                    yield min_item.afunc(*min_item.args)
                else:
                    return

    def put(self, request_ts: float, afunc: Callable[..., Coroutine[AbstractWynnResponse[Any], Any, Any]], *args: Any) -> bool:
        with self._lock:
            _item = _RequestItem(request_ts, afunc, args)
            if _item in self._list:
                return False
            self._list.append(_item)
            return True

    @property
    def length(self) -> int:
        return len(self._list)
