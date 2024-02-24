from __future__ import annotations
from typing import TYPE_CHECKING

from .. import DateColumn

if TYPE_CHECKING:
    from datetime import datetime as dt


class GuildHistoryId:

    def __init__(self, name: str, datetime: dt | DateColumn) -> None:
        self._name = name
        self._datetime = datetime if isinstance(datetime, DateColumn) else DateColumn(datetime)

    @property
    def name(self) -> str:
        return self._name

    @property
    def datetime(self) -> DateColumn:
        return self._datetime
