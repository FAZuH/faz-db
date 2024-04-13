from typing import Any

from dotenv import dotenv_values


class Config:

    _debug: bool
    _db_username: str
    _db_password: str
    _db_max_retries: int
    _schema_name: str
    _issues_webhook: str
    _error_log_file: str
    _status_report_webhook: str

    @classmethod
    def load_config(cls) -> None:
        config = dotenv_values(".env")  # default type for values is str | None
        cls._debug = bool(int(cls._must_get(config, "DEBUG")))
        cls._db_username = cls._must_get(config, "DB_USERNAME")
        cls._db_password = cls._must_get(config, "DB_PASSWORD")
        cls._db_max_retries = int(cls._must_get(config, "DB_MAX_RETRIES"))
        cls._schema_name = cls._must_get(config, "SCHEMA_NAME")
        cls._issues_webhook = cls._must_get(config, "ISSUES_WEBHOOK")
        cls._error_log_file = cls._must_get(config, "ERROR_LOG_FILE")
        cls._status_report_webhook = cls._must_get(config, "STATUS_REPORT_WEBHOOK")

    @staticmethod
    def _must_get(dict_: dict[str, str | None], key: str) -> Any:
        value = dict_.get(key)
        if value is None:
            raise ValueError(f"Missing required config key: {key}")
        return value

    @classmethod
    def get_is_debug(cls) -> bool:
        return cls._debug

    @classmethod
    def get_db_username(cls) -> str:
        return cls._db_username

    @classmethod
    def get_db_password(cls) -> str:
        return cls._db_password

    @classmethod
    def get_db_max_retries(cls) -> int:
        return cls._db_max_retries

    @classmethod
    def get_schema_name(cls) -> str:
        return cls._schema_name

    @classmethod
    def get_issues_webhook(cls) -> str:
        return cls._issues_webhook

    @classmethod
    def get_error_log_file(cls) -> str:
        return cls._error_log_file

    @classmethod
    def get_status_report_webhook(cls) -> str:
        return cls._status_report_webhook
