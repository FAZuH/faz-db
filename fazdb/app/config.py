import os
from typing import Callable

from dotenv import load_dotenv


class Config:

    admin_discord_id: int
    
    discord_log_webhook: str
    discord_status_webhook: str

    fazdb_db_max_retries: int

    mysql_host: str
    mysql_port: int
    mysql_username: str
    mysql_password: str
    fazdb_db_name: str

    @classmethod
    def read(cls) -> None:
        load_dotenv()

        cls.admin_discord_id = cls.__must_get_env("ADMIN_DISCORD_ID", int)

        cls.discord_log_webhook = cls.__must_get_env("DISCORD_LOG_WEBHOOK")
        cls.discord_status_webhook = cls.__must_get_env("DISCORD_STATUS_WEBHOOK")

        cls.fazdb_db_max_retries = cls.__must_get_env("FAZDB_DB_MAX_RETRIES", int)

        cls.mysql_host = cls.__must_get_env("MYSQL_HOST")
        cls.mysql_port = cls.__must_get_env("MYSQL_PORT", int)
        cls.mysql_username = cls.__must_get_env("MYSQL_USER")
        cls.mysql_password = cls.__must_get_env("MYSQL_PASSWORD")
        cls.fazdb_db_name = cls.__must_get_env("MYSQL_FAZDB_DATABASE")

    @staticmethod
    def __must_get_env[T](key: str, type_strategy: Callable[[str], T] = str) -> T:
        try:
            env = os.getenv(key)
            return type_strategy(env)  # type: ignore
        except ValueError:
            raise ValueError(f"Failed parsing environment variable {key} into type {type_strategy}")
