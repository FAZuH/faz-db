from loguru import logger  # type: ignore

from dotenv import dotenv_values


config: dict[str, str] = dotenv_values(".env")  # type: ignore


# Vindicator
__version__ = "0.0.1"
__author__ = "FAZuH"
