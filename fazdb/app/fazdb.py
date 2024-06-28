from __future__ import annotations
from typing import TYPE_CHECKING

from fazdb.api import WynnApi
from fazdb.config import Config
from fazdb.db import DatabaseQuery
from fazdb.db.fazdb import FazDbDatabase
from fazdb.heartbeat import SimpleHeartbeat
from fazdb.logger import FazDbLogger

from . import App

if TYPE_CHECKING:
    from fazdb.db.fazdb import IFazDbDatabase
    from fazdb import Api, Heartbeat, Logger, IFazDbDatabase


class FazDb(App):

    def __init__(self) -> None:
        config = Config()
        config.read()

        self._logger = FazDbLogger()

        self._api = WynnApi(self.logger)

        fazdb_query = DatabaseQuery(
            config.mysql_username,
            config.mysql_password,
            config.fazdb_db_name,
            config.fazdb_db_max_retries
        )
        self._db = FazDbDatabase(self.logger, fazdb_query)

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
    def db(self) -> IFazDbDatabase:
        return self._db

    @property
    def heartbeat(self) -> Heartbeat:
        return self._heartbeat

    @property
    def logger(self) -> Logger:
        return self._logger
