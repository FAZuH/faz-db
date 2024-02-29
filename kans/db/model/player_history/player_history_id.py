from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

from .. import DateColumn

if TYPE_CHECKING:
    from datetime import datetime as dt

class PlayerHistoryId:

    def __init__(self, uuid: str, datetime: dt | DateColumn) -> None:
        self._uuid = uuid
        self._datetime = datetime if isinstance(datetime, DateColumn) else DateColumn(datetime)

    class IdType(TypedDict):
        uuid: str
        datetime: dt

    @property
    def uuid(self) -> str:
        return self._uuid

    @property
    def datetime(self) -> DateColumn:
        return self._datetime
