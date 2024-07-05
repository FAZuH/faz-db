from __future__ import annotations
from threading import Thread
from typing import TYPE_CHECKING

from . import Heartbeat, HeartbeatTask
from .task import RequestQueue, ResponseQueue, TaskApiRequest, TaskDbInsert

if TYPE_CHECKING:
    from .task import Task
    from fazdb import Api, IFazdbDatabase


class SimpleHeartbeat(Thread, Heartbeat):

    def __init__(self, api: Api, db: IFazdbDatabase) -> None:
        super().__init__(target=self.run, daemon=True)
        self._tasks: list[HeartbeatTask] = []

        request_list = RequestQueue()
        response_list = ResponseQueue()

        api_request = TaskApiRequest(api, request_list, response_list)
        db_insert = TaskDbInsert(api, db, request_list, response_list)

        self._add_task(api_request)
        self._add_task(db_insert)

    def start(self) -> None:
        for task in self._tasks:
            task.start()

    def stop(self) -> None:
        for task in self._tasks:
            task.cancel()

    def _add_task(self, task: Task) -> None:
        self._tasks.append(HeartbeatTask(task))
