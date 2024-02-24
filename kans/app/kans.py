from __future__ import annotations
from typing import TYPE_CHECKING

from dotenv import dotenv_values
from loguru import logger

from .app import App
from kans.api import WynnApi
from kans.db import WynndataDatabase
from kans.heartbeat import SimpleHeartbeat

if TYPE_CHECKING:
    from loguru import Logger
    from kans import ConfigT
    from kans.api import Api
    from kans.db import Database
    from kans.heartbeat import Heartbeat


class Kans(App):

    def __init__(self) -> None:
        self._config: ConfigT = dotenv_values(".env")  # type: ignore
        self._logger: Logger = logger
        self._wynnapi: Api = WynnApi()
        self._wynnrepo: Database = WynndataDatabase(self.config, self.logger)
        self._heartbeat: Heartbeat = SimpleHeartbeat(self)

    def start(self) -> None:
        self.logger.info("Starting Heartbeat")
        self.heartbeat.start()

    def stop(self) -> None:
        self.logger.info("Stopping Heartbeat")
        self.heartbeat.stop()

    @property
    def config(self) -> ConfigT:
        return self._config

    @property
    def heartbeat(self) -> Heartbeat:
        return self._heartbeat

    @property
    def logger(self) -> Logger:
        return self._logger

    @property
    def wynnapi(self) -> Api:
        return self._wynnapi

    @property
    def wynnrepo(self) -> Database:
        return self._wynnrepo
