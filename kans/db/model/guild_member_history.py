from __future__ import annotations
from typing import TYPE_CHECKING

from kans import DateColumn, UuidColumn

if TYPE_CHECKING:
    from datetime import datetime as dt


class GuildMemberHistory:
    """implements `GuildMemberHistoryId`

    id: `uuid`, `datetime`"""

    def __init__(
        self,
        uuid: bytes | UuidColumn,
        contributed: int,
        joined: dt | DateColumn,
        datetime: dt | DateColumn
    ) -> None:
        self._uuid = uuid if isinstance(uuid, UuidColumn) else UuidColumn(uuid)
        self._contributed = contributed
        self._joined = joined if isinstance(joined, DateColumn) else DateColumn(joined)
        self._datetime = datetime if isinstance(datetime, DateColumn) else DateColumn(datetime)

    @property
    def uuid(self) -> UuidColumn:
        return self._uuid

    @property
    def contributed(self) -> int:
        return self._contributed

    @property
    def joined(self) -> DateColumn:
        return self._joined

    @property
    def datetime(self) -> DateColumn:
        return self._datetime
