from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from loguru import Logger
    from kans import Database, Api
    from constants import ConfigT


class App(Protocol):
    """<<interface>>"""
    @property
    def config(self) -> ConfigT: ...
    @property
    def logger(self) -> Logger: ...
    @property
    def wynnapi(self) -> Api: ...
    @property
    def wynnrepo(self) -> Database: ...
