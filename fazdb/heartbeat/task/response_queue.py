from __future__ import annotations
from threading import Lock
from typing import TYPE_CHECKING, Any, Iterable

if TYPE_CHECKING:
    from fazdb.api import BaseResponse
    type BaseResponse_ = BaseResponse[Any, Any]


class ResponseQueue:

    def __init__(self):
        self._list: list[BaseResponse_] = []
        self._lock = Lock()

    def get(self) -> list[BaseResponse_]:
        with self._lock:
            ret = self._list
            self._list = []
        return ret

    def put(self, responses: Iterable[BaseResponse_]) -> None:
        with self._lock:
            self._list.extend(responses)
