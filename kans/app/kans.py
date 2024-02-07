from __future__ import annotations
from typing import TYPE_CHECKING, Any

from dotenv import dotenv_values
from loguru import logger

from kans import App, HeartBeat, WynnApi, WynnDataDatabase

if TYPE_CHECKING:
    from loguru import Logger
    from kans import Api, Database


class Kans(App):

    def __init__(self) -> None:
        self._config: dict[str, Any] = dotenv_values(".env")
        self._logger: Logger = logger
        self._wynnapi: Api = WynnApi()
        self._wynnrepo: Database = WynnDataDatabase(self.config, self.logger)

        self._heartbeat: HeartBeat = HeartBeat(self)

    def start(self) -> None:
        self.logger.info("Starting HeartBeat")
        self._heartbeat.start()

    @property
    def config(self) -> dict[str, Any]:
        return self._config

    @property
    def heartbeat(self) -> HeartBeat:
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
