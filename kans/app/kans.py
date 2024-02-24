from __future__ import annotations
from typing import TYPE_CHECKING

from dotenv import dotenv_values
from loguru import logger

from kans import App, Heartbeat, WynnApi, WynnDataDatabase

if TYPE_CHECKING:
    from loguru import Logger
    from kans import Api, Database
    from constants import ConfigT


class Kans(App):

    def __init__(self) -> None:
        self._config: ConfigT = dotenv_values(".env")  # type: ignore
        self._logger: Logger = logger
        self._wynnapi: Api = WynnApi()
        self._wynnrepo: Database = WynnDataDatabase(self.config, self.logger)
        self._heartbeat: Heartbeat = Heartbeat(self)

    def start(self) -> None:
        self.logger.info("Starting HeartBeat")
        self._heartbeat.start()

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
