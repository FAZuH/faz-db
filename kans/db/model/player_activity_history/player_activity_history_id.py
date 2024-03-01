from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

from .. import DateColumn, UuidColumn

if TYPE_CHECKING:
    from datetime import datetime


class PlayerActivityHistoryId:

    def __init__(self, uuid: bytes | UuidColumn, logon_datetime: datetime | DateColumn) -> None:
        self._uuid: UuidColumn = uuid if isinstance(uuid, UuidColumn) else UuidColumn(uuid)
        self._logon_datetime = logon_datetime if isinstance(logon_datetime, DateColumn) else DateColumn(logon_datetime)

    class IdType(TypedDict):
        uuid: bytes
        logon_datetime: datetime

    @property
    def logon_datetime(self) -> DateColumn:
        return self._logon_datetime

    @property
    def uuid(self) -> UuidColumn:
        return self._uuid