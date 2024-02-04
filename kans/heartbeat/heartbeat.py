from __future__ import annotations
from threading import Thread
from typing import TYPE_CHECKING

from kans import (
    FetchCoreTask,
    FetchGuildTask,
    FetchOnlineTask,
    FetchPlayerTask,
    HeartBeatTask,
    RequestQueue,
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
        fetch_guild = FetchGuildTask(app, request_queue)
        fetch_online = FetchOnlineTask(app, request_queue)
        fetch_player = FetchPlayerTask(app, request_queue)

        self._add_task(FetchCoreTask(app, fetch_guild, fetch_online, fetch_player, request_queue))
        self._add_task(fetch_guild)
        self._add_task(fetch_online)
        self._add_task(fetch_player)

    def _add_task(self, task: TaskBase) -> None:
        self._tasks.append(HeartBeatTask(self._logger, task))

    def run(self) -> None:
        for task in self._tasks:
            task.start()

    def stop(self) -> None:
        for task in self._tasks:
            task.cancel()
