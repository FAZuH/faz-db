from dotenv import dotenv_values


class Config:

    # def __init__(self, config: dict[str, str | None]) -> None:
    def __init__(self) -> None:
        config = dotenv_values(".env")
        self._db_username = self._must_get(config, "DB_USERNAME")
        self._db_password = self._must_get(config, "DB_PASSWORD")
        self._schema_name = self._must_get(config, "SCHEMA_NAME")
        self._issues_webhook = self._must_get(config, "ISSUES_WEBHOOK")
        self._error_log_file = self._must_get(config, "ERROR_LOG_FILE")
        self._status_report_webhook = self._must_get(config, "STATUS_REPORT_WEBHOOK")

    def _must_get(self, dict_: dict[str, str | None], key: str) -> str:
        value = dict_.get(key)
        if value is None:
            raise ValueError(f"Missing required config key: {key}")
        return value

    @property
    def db_username(self) -> str:
        return self._db_username

    @property
    def db_password(self) -> str:
        return self._db_password

    @property
    def schema_name(self) -> str:
        return self._schema_name

    @property
    def issues_webhook(self) -> str:
        return self._issues_webhook

    @property
    def error_log_file(self) -> str:
        return self._error_log_file

    @property
    def status_report_webhook(self) -> str:
        return self._status_report_webhook
