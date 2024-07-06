from __future__ import annotations
from datetime import datetime
from typing import Any, Coroutine, TYPE_CHECKING
from typing import Coroutine

if TYPE_CHECKING:
    from fazdb.api.wynn.response import AbstractWynnResponse


type WynnRespCoro = Coroutine[AbstractWynnResponse[Any], Any, Any]


class RequestItem:

    def __init__(
        self,
        coro: WynnRespCoro,
        priority: int,
        req_ts: float,
    ) -> None:
        self._req_ts = req_ts
        self._coro = coro
        self._priority = priority

    def is_eligible(self, timestamp: None | float = None) -> bool:
        timestamp = timestamp or datetime.now().timestamp()
        return self.req_ts < timestamp

    def __eq__(self, other: object | RequestItem) -> bool:
        if isinstance(other, RequestItem):
            return (
                (self.coro.cr_frame.f_locals == other.coro.cr_frame.f_locals) and  # type: ignore
                (self.coro.__qualname__ == other.coro.__qualname__)
            )
        return False

    def __lt__(self, other: RequestItem) -> bool:
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
    def coro(self) -> WynnRespCoro:
        return self._coro

    @property
    def priority(self) -> int:
        return self._priority
