from typing import TypedDict

from dotenv import dotenv_values

ConfigT = TypedDict("ConfigT", {
    "WYNNDATA_DB_USER": str,
    "WYNNDATA_DB_PASSWORD": str,
    "WYNNDATA_SCHEMA_NAME": str,
    "DATABASE_WEBHOOK": str,
    "ERROR_WEBHOOK": str,
    "WYNNAPI_FETCHER_WEBHOOK": str,
    "WYNNDATA_LOGGER_WEBHOOK": str,
})


config: ConfigT = dotenv_values(".env")  # type: ignore
__version__ = "0.0.1"
__author__ = "FAZuH"
