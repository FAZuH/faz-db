from __future__ import annotations
from typing import TYPE_CHECKING

from . import KansUptimeId

if TYPE_CHECKING:
    from datetime import datetime as dt


class KansUptime(KansUptimeId):

    def __init__(self, start_time: dt, stop_time: dt) -> None:
        self._start_time = start_time
        self._stop_time = stop_time

    @property
    def start_time(self) -> dt:
        return self._start_time

    @property
    def stop_time(self) -> dt:
        return self._stop_time
