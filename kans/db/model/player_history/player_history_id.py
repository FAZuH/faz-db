from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

from .. import DateColumn, UuidColumn

if TYPE_CHECKING:
    from datetime import datetime as dt

class PlayerHistoryId:

    def __init__(self, uuid: bytes | UuidColumn, datetime: dt | DateColumn) -> None:
        self._uuid = uuid if isinstance(uuid, UuidColumn) else UuidColumn(uuid)
        self._datetime = datetime if isinstance(datetime, DateColumn) else DateColumn(datetime)

    def to_dict(self) -> PlayerHistoryId.Type:
        return {
                "uuid": self.uuid.uuid,
                "datetime": self.datetime.datetime
        }

    class Type(TypedDict):
        uuid: bytes
        datetime: dt

    @property
    def uuid(self) -> UuidColumn:
        return self._uuid

    @property
    def datetime(self) -> DateColumn:
        return self._datetime
