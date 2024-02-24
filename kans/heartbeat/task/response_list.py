from __future__ import annotations
from threading import Lock
from typing import TYPE_CHECKING, Any, Generator, Iterable

if TYPE_CHECKING:
    from kans import WynnResponse


class ResponseList:

    def __init__(self):
        self._list: list[Any] = []
        self._lock: Lock = Lock()

    def get(self) -> Generator[WynnResponse[Any], Any, None]:
        with self._lock:
            while len(self._list) > 0:
                yield self._list.pop(0)

    def put(self, responses: Iterable[WynnResponse[Any]]) -> None:
        with self._lock:
            self._list.extend(list(responses))
