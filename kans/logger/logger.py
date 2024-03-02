from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from . import ConsoleLogger, DiscordLogger, PerformanceLogger
    from kans import ConfigT


class Logger(Protocol):
    def __init__(self, config: ConfigT) -> None: ...
    def set_up(self) -> None: ...
    @property
    def console(self) -> ConsoleLogger: ...
    @property
    def discord(self) -> DiscordLogger: ...
    @property
    def performance(self) -> PerformanceLogger: ...
