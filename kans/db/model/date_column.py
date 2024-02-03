from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime as dt


class DateColumn:

    _MYSQL_DT_FMT: str = "%Y-%m-%d %H:%M:%S"

    def __init__(self, datetime: dt):
        self._datetime = datetime

    def to_sqldt(self) -> str:
        return self._datetime.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def datetime(self) -> dt:
        return self._datetime

    @property
    def mysql_dt_fmt(self) -> str:
        return self._MYSQL_DT_FMT
