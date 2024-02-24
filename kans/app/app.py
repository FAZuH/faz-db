from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

from kans.heartbeat import Heartbeat

if TYPE_CHECKING:
    from loguru import Logger
    from kans.api import Api
    from kans.db import Database
    from constants import ConfigT


class App(Protocol):
    """<<interface>>"""
    def start(self) -> None: ...
    def stop(self) -> None: ...
    @property
    def config(self) -> ConfigT: ...
    @property
    def heartbeat(self) -> Heartbeat: ...
    @property
    def logger(self) -> Logger: ...
    @property
    def api(self) -> Api: ...
    @property
    def db(self) -> Database: ...
