from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

from . import GuildMemberHistoryId
from .. import DateColumn

if TYPE_CHECKING:
    from datetime import datetime


class GuildMemberHistory(GuildMemberHistoryId):
    """implements `GuildMemberHistoryId`

    id: `uuid`, `datetime`"""

    def __init__(
        self,
        uuid: str,
        contributed: int,
        joined: datetime | DateColumn,
        datetime: datetime | DateColumn
    ) -> None:
        super().__init__(uuid, datetime)
        self._contributed = contributed
        self._joined = joined if isinstance(joined, DateColumn) else DateColumn(joined)

    class Type(TypedDict):
        uuid: str
        contributed: int
        joined: datetime
        datetime: datetime

    @property
    def contributed(self) -> int:
        return self._contributed

    @property
    def joined(self) -> DateColumn:
        return self._joined
