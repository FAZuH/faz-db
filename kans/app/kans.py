from __future__ import annotations
from typing import TYPE_CHECKING

from dotenv import dotenv_values

from .app import App
from kans.api import WynnApi
from kans.db import KansDatabase
from kans.heartbeat import SimpleHeartbeat
from kans.logger import KansLogger

if TYPE_CHECKING:
    from kans import Api, ConfigT, Database, Heartbeat, Logger


class Kans(App):

    def __init__(self) -> None:
        self._config: ConfigT = dotenv_values(".env")  # type: ignore
        self._logger = KansLogger(self.config)
        self._api = WynnApi(self.logger)
        self._db = KansDatabase(self.config, self.logger)
        self._heartbeat = SimpleHeartbeat(self.config, self.logger, self.api, self.db)

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
    def config(self) -> ConfigT:
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
