from . import (
    ConsoleLogger,
    DiscordLogger,
    Logger,
    PerformanceLogger
)


class WynnDbLogger(Logger):

    def __init__(self) -> None:
        self._console_logger = ConsoleLogger()
        self._discord_logger = DiscordLogger(self._console_logger)
        self._performance_logger = PerformanceLogger()

    def set_up(self) -> None:
        return

    @property
    def console(self) -> ConsoleLogger:
        return self._console_logger

    @property
    def discord(self) -> DiscordLogger:
        return self._discord_logger

    @property
    def performance(self) -> PerformanceLogger:
        return self._performance_logger
