from __future__ import annotations
from typing import TYPE_CHECKING

from . import App
from wynndb import Config
from wynndb.api import WynnApi
from wynndb.db import KansDatabase
from wynndb.heartbeat import SimpleHeartbeat
from wynndb.logger import KansLogger

if TYPE_CHECKING:
    from wynndb import Api, Database, Heartbeat, Logger


class Kans(App):

    def __init__(self) -> None:
        self._config = Config()
        self._logger = KansLogger(self.config)
        self._api = WynnApi(self.logger)
        self._db = KansDatabase(self.config, self.logger)
        self._heartbeat = SimpleHeartbeat(self.api, self.config, self.db, self.logger)

    def start(self) -> None:
        self.logger.console.info("Starting Kans Heartbeat...")
        self.heartbeat.start()

    def stop(self) -> None:
        self.logger.console.info("Stopping Heartbeat...")
        self.heartbeat.stop()

    @property
    def api(self) -> Api:
        return self._api

    @property
    def config(self) -> Config:
        return self._config

    @property
    def db(self) -> Database:
        return self._db

    @property
    def heartbeat(self) -> Heartbeat:
        return self._heartbeat

    @property
    def logger(self) -> Logger:
        return self._logger