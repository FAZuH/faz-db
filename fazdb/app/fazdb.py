from __future__ import annotations
from typing import Any, Callable, TYPE_CHECKING

from loguru import logger

from fazdb.api import WynnApi
from fazdb.db.fazdb import FazdbDatabase
from fazdb.heartbeat import SimpleHeartbeat
from fazdb.util import RetryHandler

from . import App, Config, Logger, Metrics

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
        self._heartbeat = SimpleHeartbeat(self.api, self.db)

        self.__register_retry_handler()
        self.__register_metric()

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
        """Registers retry handler to this appp"""
        register_lambda: Callable[[Callable[..., Any]], None] = lambda func: RetryHandler.register(
            func, self.config.fazdb_db_max_retries, Exception
        )
        
        # Register retry handler to database
        repositories = self.db.repositories
        for repo in repositories:
            register_lambda(repo.table_disk_usage)
            register_lambda(repo.create_table)
            register_lambda(repo.insert)
            register_lambda(repo.delete)
            register_lambda(repo.is_exists)

    def __register_metric(self) -> None:
        metric = Metrics()

        # Summary metrics
        metric.register_summary(
            self.api.guild.get,
            "wapi_request_guild_seconds",
            "Wynncraft API total request duration on endpoint 'Guild'"
        )
        metric.register_summary(
            self.api.player.get_online_uuids,
            "wapi_request_onlineplayers_seconds",
            "Wynncraft API total request duration on endpoint 'Online Players'"
        )
        metric.register_summary(
            self.api.player.get_full_stats,
            "wapi_request_player_seconds",
            "Wynncraft API total request duration on endpoint 'Player'"
        )

        # Counter metrics
        metric.register_counter(
            self.api.guild.get,
            "wapi_request_guild_count",
            "Wynncraft API request count on endpoint 'Guild'"
        )
        metric.register_counter(
            self.api.player.get_online_uuids,
            "wapi_request_onlineplayers_count",
            "Wynncraft API request count on endpoint 'Online Players'"
        )
        metric.register_counter(
            self.api.player.get_full_stats,
            "wapi_request_player_count",
            "Wynncraft API request count on endpoint 'Player'"
        )

        metric.start()
