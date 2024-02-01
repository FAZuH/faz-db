from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING
from typing_extensions import override

from vindicator import GuildHistoryId

if TYPE_CHECKING:
    from datetime import datetime as dt
    from vindicator import GuildResponse


class GuildHistory(GuildHistoryId):
    """id: name, datetime"""

    def __init__(
        self,
        name: str,
        level: Decimal,
        territories: int,
        wars: int,
        member_total: int,
        online_members: int,
        datetime: dt
    ) -> None:
        self._name = name
        self._level = level
        self._territories = territories
        self._wars = wars
        self._member_total = member_total
        self._online_members = online_members
        self._datetime = datetime

    @classmethod
    def from_response(cls, response: GuildResponse) -> GuildHistory:
        return cls(
            name=response.body.name,
            level=Decimal(response.body.level),
            territories=response.body.territories,
            wars=response.body.wars,
            member_total=response.body.members.total,
            online_members=response.body.members.get_online_members(),
            datetime=response.get_datetime()
        )

    @property
    @override
    def name(self) -> str:
        return self._name

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

    @property
    @override
    def datetime(self) -> dt:
        return self._datetime
