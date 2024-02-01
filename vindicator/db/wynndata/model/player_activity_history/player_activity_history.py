from __future__ import annotations
from typing import TYPE_CHECKING
from typing_extensions import override

from vindicator import DateColumn, PlayerActivityHistoryId, UuidColumn

if TYPE_CHECKING:
    from vindicator import PlayerResponse


class PlayerActivityHistory(PlayerActivityHistoryId):
    """id: uuid, logon_datetime"""

    def __init__(
        self,
        uuid: UuidColumn,
        logon_datetime: DateColumn,
        logoff_datetime: DateColumn
    ) -> None:
        self._uuid = uuid
        self._logon_datetime = logon_datetime
        self._logoff_datetime = logoff_datetime

    @classmethod
    def from_responses(cls, response: PlayerResponse) -> PlayerActivityHistory:
        raise NotImplementedError

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
