from __future__ import annotations
from typing import Any, Callable, TYPE_CHECKING

from loguru import logger

from fazdb.api import WynnApi
from fazdb.db.fazdb import FazdbDatabase
from fazdb.heartbeat import SimpleHeartbeat
from fazdb.util import RetryHandler

from . import App, Config, Logger

if TYPE_CHECKING:
    from fazdb import Api, Heartbeat, IFazdbDatabase


class FazDb(App):

    def __init__(self) -> None:
        self._config = Config()
        self._config.read()
        Logger.setup(self._config.discord_log_webhook)

        self._api = WynnApi()

        self._db = FazdbDatabase(
            "mysql+aiomysql",
            self._config.mysql_username,
            self._config.mysql_password,
            self._config.mysql_host,
            self._config.mysql_port,
            self._config.fazdb_db_name
        )
        self.__register_retry_handler()

        self._heartbeat = SimpleHeartbeat(self.api, self.db)

    def start(self) -> None:
        logger.info("Starting WynnDb Heartbeat...")
        self.heartbeat.start()

    def stop(self) -> None:
        logger.info("Stopping Heartbeat...")
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

    def __register_retry_handler(self) -> None:
        """Helper method to register retry handlers on faz-db Database.
        Call this method right after instantiating IFazdbDatabase."""
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
