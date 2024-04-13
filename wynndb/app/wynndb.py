from __future__ import annotations
from typing import TYPE_CHECKING

from . import App
from wynndb.api import WynnApi
from wynndb.db import WynnDbDatabase
from wynndb.heartbeat import SimpleHeartbeat
from wynndb.logger import WynnDbLogger

if TYPE_CHECKING:
    from wynndb import Api, Database, Heartbeat, Logger


class WynnDb(App):

    def __init__(self) -> None:
        self._logger = WynnDbLogger()
        self._api = WynnApi(self.logger)
        self._db = WynnDbDatabase(self.logger)
        self._heartbeat = SimpleHeartbeat(self.api, self.db, self.logger)

    def start(self) -> None:
        self.logger.console.info("Starting WynnDb Heartbeat...")
        self.heartbeat.start()

    def stop(self) -> None:
        self.logger.console.info("Stopping Heartbeat...")
        self.heartbeat.stop()

    @property
    def api(self) -> Api:
        return self._api

    @property
    def db(self) -> Database:
        return self._db

    @property
    def heartbeat(self) -> Heartbeat:
        return self._heartbeat

    @property
    def logger(self) -> Logger:
        return self._logger
