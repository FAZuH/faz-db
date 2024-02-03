from __future__ import annotations
import threading
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src import AbstractRequest


class FetchQueue:

    def __init__(self) -> None:
        self._queue: list[AbstractRequest[Any]] = []
        self._lock: threading.Lock = threading.Lock()

    def put(self, entry: AbstractRequest[Any]) -> bool:
        if entry in self._queue:
            return False
        self._queue.append(entry)
        return True

    def get(self, amount: int) -> list[AbstractRequest[Any]]:
        ret: list[AbstractRequest[Any]] = []
        for _ in range(amount):
            with self._lock:
                if len(self._queue) == 0:
                    break
                lowest: AbstractRequest[Any] = min(self._queue)  # AbstractRequest implements __lt__()
                self._queue.remove(lowest)
                ret.append(lowest)
        return ret

    def __contains__(self, item: str) -> bool:
        return item in self._queue  # type: ignore AbstractRequest implements __eq__()
