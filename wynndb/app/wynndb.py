from __future__ import annotations
from typing import TYPE_CHECKING

from wynndb.api import WynnApi
from wynndb.config import Config
from wynndb.db import DatabaseQuery
from wynndb.db.wynndb import WynnDbDatabase
from wynndb.heartbeat import SimpleHeartbeat
from wynndb.logger import WynnDbLogger

from . import App

if TYPE_CHECKING:
    from wynndb.db.wynndb import IWynnDbDatabase
    from wynndb import Api, Heartbeat, Logger, IWynnDbDatabase


class WynnDb(App):

    def __init__(self) -> None:
        Config.load_config()
        self._logger = WynnDbLogger()

        self._api = WynnApi(self.logger)

        wynndb_query = DatabaseQuery(
            Config.get_db_username(),
            Config.get_db_password(),
            Config.get_schema_name(),
            Config.get_db_max_retries()
        )
        self._db = WynnDbDatabase(self.logger, wynndb_query)

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
    def db(self) -> IWynnDbDatabase:
        return self._db

    @property
    def heartbeat(self) -> Heartbeat:
        return self._heartbeat

    @property
    def logger(self) -> Logger:
        return self._logger
