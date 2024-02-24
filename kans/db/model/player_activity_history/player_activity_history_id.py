from __future__ import annotations
from typing import TYPE_CHECKING

from .. import DateColumn, UuidColumn

if TYPE_CHECKING:
    from datetime import datetime as dt


class PlayerActivityHistoryId:

    def __init__(self, uuid: str | UuidColumn, logon_datetime: dt | DateColumn) -> None:
        self._uuid: UuidColumn = uuid if isinstance(uuid, UuidColumn) else UuidColumn.from_str(uuid)
        self._logon_datetime = logon_datetime if isinstance(logon_datetime, DateColumn) else DateColumn(logon_datetime)

    @property
    def logon_datetime(self) -> DateColumn:
        return self._logon_datetime

    @property
    def uuid(self) -> UuidColumn:
        return self._uuid