from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

from kans.db.model import DateColumn

if TYPE_CHECKING:
    from datetime import datetime as datetime


class KansUptimeId:

    def __init__(self, start_time: datetime | DateColumn) -> None:
        self._start_time = start_time if isinstance(start_time, DateColumn) else DateColumn(start_time)

    class TypeId(TypedDict):
        start_time: datetime

    @property
    def start_time(self) -> DateColumn:
        return self._start_time
