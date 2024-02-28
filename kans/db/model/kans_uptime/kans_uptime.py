from __future__ import annotations
from typing import TYPE_CHECKING, Any

from . import KansUptimeId
from .. import DateColumn

if TYPE_CHECKING:
    from datetime import datetime as dt


class KansUptime(KansUptimeId):

    def __init__(self, start_time: dt | DateColumn, stop_time: dt | DateColumn) -> None:
        self._start_time = start_time if isinstance(start_time, DateColumn) else DateColumn(start_time)
        self._stop_time = stop_time if isinstance(stop_time, DateColumn) else DateColumn(stop_time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "start_time": self.start_time.datetime,
            "stop_time": self.stop_time.datetime
        }

    @property
    def start_time(self) -> DateColumn:
        return self._start_time

    @property
    def stop_time(self) -> DateColumn:
        return self._stop_time
