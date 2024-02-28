from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

from .. import DateColumn

if TYPE_CHECKING:
    from datetime import datetime


class GuildHistoryId:

    def __init__(self, name: str, datetime: datetime | DateColumn) -> None:
        self._name = name
        self._datetime = datetime if isinstance(datetime, DateColumn) else DateColumn(datetime)

    def to_dict(self) -> GuildHistoryId.Type:
        return {
                "name": self.name,
                "datetime": self.datetime.datetime
        }

    class Type(TypedDict):
        name: str
        datetime: datetime

    @property
    def name(self) -> str:
        return self._name

    @property
    def datetime(self) -> DateColumn:
        return self._datetime
