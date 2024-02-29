from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

from . import PlayerActivityHistoryId
from .. import DateColumn

if TYPE_CHECKING:
    from .. import UuidColumn
    from datetime import datetime


class PlayerActivityHistory(PlayerActivityHistoryId):
    """implements

    id: `uuid`, `logon_datetime`
    """

    def __init__(
        self,
        uuid: str | UuidColumn,
        logon_datetime: datetime | DateColumn,
        logoff_datetime: datetime | DateColumn
    ) -> None:
        super().__init__(uuid, logon_datetime)
        self._logoff_datetime = logoff_datetime if isinstance(logoff_datetime, DateColumn) else DateColumn(logoff_datetime)

    class Type(TypedDict):
        uuid: bytes
        logon_datetime: datetime
        logoff_datetime: datetime

    @property
    def logoff_datetime(self) -> DateColumn:
        return self._logoff_datetime
