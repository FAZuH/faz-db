from dotenv import dotenv_values
from loguru import logger  # type: ignore


config: dict[str, str] = dotenv_values(".env")  # type: ignore

__version__ = "0.0.1"
__author__ = "FAZuH"
