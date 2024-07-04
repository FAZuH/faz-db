from __future__ import annotations
from typing import Any, Callable, TYPE_CHECKING

from fazdb.api import WynnApi
from fazdb.db.fazdb import FazdbDatabase
from fazdb.heartbeat import SimpleHeartbeat
from fazdb.logger import FazDbLogger
from fazdb.util import RetryHandler

from . import App, Config

if TYPE_CHECKING:
    from fazdb import Api, Heartbeat, IFazdbDatabase, Logger


class FazDb(App):

    def __init__(self) -> None:
        self._config = Config()
        self._config.read()

        self._logger = FazDbLogger()

        self._api = WynnApi(self.logger)

        self._db = FazdbDatabase(
            "mysql+aiomysql",
            self._config.mysql_username,
            self._config.mysql_password,
            self._config.mysql_host,
            self._config.mysql_port,
            self._config.fazdb_db_name
        )
        self.__register_retry_handler()

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
    def config(self) -> Config:
        return self._config

    @property
    def db(self) -> IFazdbDatabase:
        return self._db

    @property
    def heartbeat(self) -> Heartbeat:
        return self._heartbeat

    @property
    def logger(self) -> Logger:
        return self._logger

    def __register_retry_handler(self) -> None:
        """Helper method to register retry handlers on faz-db Database.
        Call this method right after instantiating IFazdbDatabase."""
        RetryHandler.set_discord_logger(self.logger.discord)
        register_lambda: Callable[[Callable[..., Any]], None] = lambda func: RetryHandler.register(
            func, self.config.fazdb_db_max_retries, Exception
        )
        repositories = self.db.repositories
        for repo in repositories:
            register_lambda(repo.table_disk_usage)
            register_lambda(repo.create_table)
            register_lambda(repo.insert)
            register_lambda(repo.delete)
            register_lambda(repo.is_exists)
