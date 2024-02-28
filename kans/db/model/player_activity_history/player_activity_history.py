from __future__ import annotations
from typing import TYPE_CHECKING, Any

from . import PlayerActivityHistoryId
from .. import DateColumn

if TYPE_CHECKING:
    from .. import UuidColumn
    from datetime import datetime as dt


class PlayerActivityHistory(PlayerActivityHistoryId):
    """implements

    id: `uuid`, `logon_datetime`
    """

    def __init__(
        self,
        uuid: str | UuidColumn,
        logon_datetime: dt | DateColumn,
        logoff_datetime: dt | DateColumn
    ) -> None:
        super().__init__(uuid, logon_datetime)
        self._logoff_datetime = logoff_datetime if isinstance(logoff_datetime, DateColumn) else DateColumn(logoff_datetime)

    def to_tuple(self) -> tuple[Any, ...]:
        return (self.uuid.uuid, self.logon_datetime.datetime, self.logoff_datetime.datetime)

    @property
    def logoff_datetime(self) -> DateColumn:
        return self._logoff_datetime
