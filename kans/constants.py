from typing import TypedDict

from dotenv import dotenv_values

ConfigT = TypedDict("ConfigT", {
    "DB_USERNAME": str,
    "DB_PASSWORD": str,
    "SCHEMA_NAME": str,

    "ERROR_WEBHOOK": str,
    "STATUS_REPORT_WEBHOOK": str,
})


config: ConfigT = dotenv_values(".env")  # type: ignore
__version__ = "0.0.1"
__author__ = "FAZuH"
