from __future__ import annotations
from threading import Lock
from typing import TYPE_CHECKING, Any, Iterable

if TYPE_CHECKING:
    from kans.api.wynn.response import AbstractWynnResponse


class ResponseQueue:

    def __init__(self):
        self._list: list[AbstractWynnResponse[Any]] = []
        self._lock = Lock()

    def get(self) -> list[AbstractWynnResponse[Any]]:
        with self._lock:
            ret = self._list
            self._list = []
        return ret

    def put(self, responses: Iterable[AbstractWynnResponse[Any]]) -> None:
        with self._lock:
            self._list.extend(responses)
