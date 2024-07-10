from __future__ import annotations
from typing import Any, Callable

from loguru import logger

from fazdb.api import WynnApi
from fazdb.db.fazdb import FazdbDatabase
from fazdb.heartbeat import Heartbeat
from fazdb.util import RetryHandler

from ._logger_setup import LoggerSetup
from ._metrics import Metrics
from .properties import Properties


class FazDb:

    def __init__(self) -> None:
        self._properties = Properties()
        p = self.properties
        p.setup()
        LoggerSetup.setup(p.LOG_DIR, p.DISCORD_LOG_WEBHOOK, p.ADMIN_DISCORD_ID)

        self._api = WynnApi()
        self._db = FazdbDatabase(
            "mysql+aiomysql",
            p.MYSQL_USERNAME,
            p.MYSQL_PASSWORD,
            p.MYSQL_HOST,
            p.MYSQL_PORT,
            p.FAZDB_DB_NAME
        )
        self._heartbeat = Heartbeat(self.api, self.db)

        self.__register_retry_handler()
        self.__register_metric()

    def start(self) -> None:
        logger.info("Starting WynnDb Heartbeat...")
        self.heartbeat.start()

    def stop(self) -> None:
        logger.info("Stopping Heartbeat...")
        self.heartbeat.stop()

    @property
    def api(self) -> WynnApi:
        return self._api

    @property
    def properties(self) -> Properties:
        return self._properties

    @property
    def db(self) -> FazdbDatabase:
        return self._db

    @property
    def heartbeat(self) -> Heartbeat:
        return self._heartbeat

    def __register_retry_handler(self) -> None:
        """Registers retry handler to this appp"""
        register_lambda: Callable[[Callable[..., Any]], None] = lambda func: RetryHandler.register(
            func, self.properties.FAZDB_DB_MAX_RETRIES, Exception
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
