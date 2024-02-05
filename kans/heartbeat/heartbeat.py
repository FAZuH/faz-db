from __future__ import annotations
from threading import Thread
from typing import TYPE_CHECKING

from kans import (
    HeartBeatTask,
    RequestQueue,
    WynnApiFetcher,
    WynnDataLogger,
)

if TYPE_CHECKING:
    from kans import App, TaskBase


class HeartBeat(Thread):

    def __init__(self, app: App) -> None:
        pass
        super().__init__(target=self.run, daemon=True)
        self._logger = app.logger

        self._tasks: list[HeartBeatTask] = []
        request_queue = RequestQueue()

        wynndatalogger = WynnDataLogger(app.logger, app.wynnapi, app.wynnrepo, request_queue)
        self._add_task(WynnApiFetcher(app.logger, app.wynnapi, wynndatalogger, request_queue))
        self._add_task(wynndatalogger)

    def _add_task(self, task: TaskBase) -> None:
        self._tasks.append(HeartBeatTask(self._logger, task))

    def run(self) -> None:
        for task in self._tasks:
            task.start()

    def stop(self) -> None:
        for task in self._tasks:
            task.cancel()
