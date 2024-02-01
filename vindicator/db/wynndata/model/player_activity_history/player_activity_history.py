from __future__ import annotations
from typing import TYPE_CHECKING
from typing_extensions import override

from vindicator import PlayerActivityHistoryId, UuidColumn

if TYPE_CHECKING:
    from datetime import datetime as dt
    from vindicator import PlayerResponse


class PlayerActivityHistory(PlayerActivityHistoryId):
    """id: uuid, logon_datetime"""

    def __init__(
        self,
        uuid: UuidColumn,
        logon_datetime: dt,
        logoff_datetime: dt
    ) -> None:
        self._uuid = uuid
        self._logon_datetime = logon_datetime
        self._logoff_datetime = logoff_datetime

    @classmethod
    def from_response(cls, response: PlayerResponse) -> PlayerActivityHistory:
        raise NotImplementedError

    @property
    @override
    def uuid(self) -> UuidColumn:
        return self._uuid

    @property
    @override
    def logon_datetime(self) -> dt:
        return self._logon_datetime

    @property
    def logoff_datetime(self) -> dt:
        return self._logoff_datetime
