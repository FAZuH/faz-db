from __future__ import annotations
from typing import TYPE_CHECKING
from typing_extensions import override

from vindicator import DateColumn, PlayerActivityHistoryId, UuidColumn

if TYPE_CHECKING:
    from datetime import datetime as dt


class PlayerActivityHistory(PlayerActivityHistoryId):
    """implements `PlayerActivityHistoryId`

    id: `uuid`, `logon_datetime`
    """

    def __init__(
        self,
        uuid: str | UuidColumn,
        logon_datetime: dt | DateColumn,
        logoff_datetime: dt | DateColumn
    ) -> None:
        self._uuid = uuid if isinstance(uuid, UuidColumn) else UuidColumn.from_str(uuid)
        self._logon_datetime = logon_datetime if isinstance(logon_datetime, DateColumn) else DateColumn(logon_datetime)
        self._logoff_datetime = logoff_datetime if isinstance(logoff_datetime, DateColumn) else DateColumn(logoff_datetime)

    @property
    @override
    def uuid(self) -> UuidColumn:
        return self._uuid

    @property
    @override
    def logon_datetime(self) -> DateColumn:
        return self._logon_datetime

    @property
    def logoff_datetime(self) -> DateColumn:
        return self._logoff_datetime
