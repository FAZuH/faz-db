from __future__ import annotations
from queue import PriorityQueue
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from vindicator import Request


class FetchQueue:

    def __init__(self) -> None:
        self._queue: PriorityQueue[tuple[float, Request[Any]]] = PriorityQueue()
        self._queued_req_args: set[str] = set()

    def put(self, entry: tuple[float, Request[Any]]) -> bool:
        if entry[1].request_arg in self._queued_req_args:
            return False
        else:
            self._queued_req_args.add(entry[1].request_arg)
            self._queue.put(entry)
            return True

    def get(self, amount: int) -> list[Request[Any]]:
        ret: list[Request[Any]] = []
        for _ in range(amount):
            if self._queue.empty():
                break
            item: tuple[float, Request[Any]] = self._queue.get()
            self._queued_req_args.remove(item[1].request_arg)
            ret.append(item[1])
        return ret

    def __contains__(self, item: str) -> bool:
        return item in self._queued_req_args