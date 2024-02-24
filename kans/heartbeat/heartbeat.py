from typing import Protocol


class Heartbeat(Protocol):
    """<<interface>>"""
    def run(self) -> None: ...
    def stop(self) -> None: ...
