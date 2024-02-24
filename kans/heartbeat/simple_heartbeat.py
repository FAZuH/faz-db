from __future__ import annotations
from threading import Thread
from typing import TYPE_CHECKING

from . import Heartbeat
from . import HeartbeatTask
from .task import (
    RequestList,
    ResponseList,
    WynnApiFetcher,
    WynndataLogger,
)

if TYPE_CHECKING:
    from kans.app import App
    from .task import Task


class SimpleHeartbeat(Thread, Heartbeat):

    def __init__(self, app: App) -> None:
        super().__init__(target=self.run, daemon=True)
        self._logger = app.logger

        self._tasks: list[HeartbeatTask] = []

        request_list = RequestList()
        response_list = ResponseList()

        self._add_task(WynnApiFetcher(app.logger, app.wynnapi, request_list, response_list))
        self._add_task(WynndataLogger(app.logger, app.wynnapi, app.wynnrepo, request_list, response_list))

    def start(self) -> None:
        for task in self._tasks:
            task.start()

    def stop(self) -> None:
        for task in self._tasks:
            task.cancel()

    def _add_task(self, task: Task) -> None:
        self._tasks.append(HeartbeatTask(self._logger, task))
