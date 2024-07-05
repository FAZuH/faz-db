from __future__ import annotations
from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from fazdb import Api, Heartbeat, IFazdbDatabase

    from . import Config


class App(Protocol):
    """<<interface>>"""
    def start(self) -> None: ...
    def stop(self) -> None: ...
    @property
    def api(self) -> Api: ...
    @property
    def db(self) -> IFazdbDatabase: ...
    @property
    def config(self) -> Config: ...
    @property
    def heartbeat(self) -> Heartbeat: ...
