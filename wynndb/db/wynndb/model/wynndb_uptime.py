from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

from . import DateColumn

if TYPE_CHECKING:
    from datetime import datetime


class WynnDbUptime:

    def __init__(self, start_time: datetime | DateColumn, stop_time: datetime | DateColumn) -> None:
        self._start_time = start_time if isinstance(start_time, DateColumn) else DateColumn(start_time)
        self._stop_time = stop_time if isinstance(stop_time, DateColumn) else DateColumn(stop_time)

    @property
    def start_time(self) -> DateColumn:
        return self._start_time

    @property
    def stop_time(self) -> DateColumn:
        return self._stop_time

    class Type(TypedDict):
        start_time: datetime
        stop_time: datetime
