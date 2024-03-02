from __future__ import annotations
from threading import Thread
from typing import TYPE_CHECKING

from . import Heartbeat,HeartbeatTask
from .task import (
    RequestList,
    ResponseList,
    TaskApiRequest,
    TaskDbInsert,
    TaskStatusReport,
)

if TYPE_CHECKING:
    from .task import Task
    from kans import Api, ConfigT, Database, Logger


class SimpleHeartbeat(Thread, Heartbeat):

    def __init__(self, config: ConfigT, logger: Logger, api: Api, db: Database) -> None:
        super().__init__(target=self.run, daemon=True)
        self._logger = logger

        self._tasks: list[HeartbeatTask] = []

        request_list = RequestList()
        response_list = ResponseList()

        api_request = TaskApiRequest(api, logger, request_list, response_list)
        db_insert = TaskDbInsert(api, db, logger, request_list, response_list)
        status_report = TaskStatusReport(config, logger, api, api_request, db, db_insert, request_list)

        self._add_task(api_request)
        self._add_task(db_insert)
        self._add_task(status_report)

    def start(self) -> None:
        for task in self._tasks:
            task.start()

    def stop(self) -> None:
        for task in self._tasks:
            task.cancel()

    def _add_task(self, task: Task) -> None:
        self._tasks.append(HeartbeatTask(self._logger, task))
