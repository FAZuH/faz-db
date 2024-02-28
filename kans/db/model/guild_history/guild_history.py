from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING, TypedDict

from . import GuildHistoryId

if TYPE_CHECKING:
    from datetime import datetime
    from .. import DateColumn


class GuildHistory(GuildHistoryId):
    """implements `GuildHistoryId`

    id: `name`, `datetime`"""

    def __init__(
        self,
        name: str,
        level: Decimal,
        territories: int,
        wars: int,
        member_total: int,
        online_members: int,
        datetime: datetime | DateColumn
    ) -> None:
        super().__init__(name, datetime)
        self._level = level
        self._territories = territories
        self._wars = wars
        self._member_total = member_total
        self._online_members = online_members

    def to_dict(self) -> GuildHistory.Type:
        return {
                "name": self.name,
                "level": self.level,
                "territories": self.territories,
                "wars": self.wars,
                "member_total": self.member_total,
                "online_members": self.online_members,
                "datetime": self.datetime.datetime
        }

    class Type(TypedDict):
        name: str
        level: Decimal
        territories: int
        wars: int
        member_total: int
        online_members: int
        datetime: datetime

    @property
    def level(self) -> Decimal:
        return self._level

    @property
    def territories(self) -> int:
        return self._territories

    @property
    def wars(self) -> int:
        return self._wars

    @property
    def member_total(self) -> int:
        return self._member_total

    @property
    def online_members(self) -> int:
        return self._online_members
