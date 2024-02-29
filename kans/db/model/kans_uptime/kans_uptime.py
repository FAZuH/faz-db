from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

from . import KansUptimeId
from .. import DateColumn

if TYPE_CHECKING:
    from datetime import datetime


class KansUptime(KansUptimeId):
    """id: `start_time`"""

    def __init__(self, start_time: datetime | DateColumn, stop_time: datetime | DateColumn) -> None:
        super().__init__(start_time)
        self._stop_time = stop_time if isinstance(stop_time, DateColumn) else DateColumn(stop_time)

    class Type(TypedDict):
        stop_time: datetime

    @property
    def stop_time(self) -> DateColumn:
        return self._stop_time
