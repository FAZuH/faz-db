from __future__ import annotations
from typing import TYPE_CHECKING, Any

from . import GuildMemberHistoryId
from .. import DateColumn

if TYPE_CHECKING:
    from datetime import datetime as dt
    from .. import UuidColumn


class GuildMemberHistory(GuildMemberHistoryId):
    """implements `GuildMemberHistoryId`

    id: `uuid`, `datetime`"""

    def __init__(
        self,
        uuid: bytes | UuidColumn,
        contributed: int,
        joined: dt | DateColumn,
        datetime: dt | DateColumn
    ) -> None:
        super().__init__(uuid, datetime)
        self._contributed = contributed
        self._joined = joined if isinstance(joined, DateColumn) else DateColumn(joined)

    def to_tuple(self) -> tuple[Any, ...]:
        return (self.uuid.uuid, self.contributed, self.joined.datetime, self.datetime.datetime)

    @property
    def contributed(self) -> int:
        return self._contributed

    @property
    def joined(self) -> DateColumn:
        return self._joined
