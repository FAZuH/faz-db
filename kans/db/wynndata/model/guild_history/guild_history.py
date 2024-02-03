from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING, Iterable
from typing_extensions import override

from src import DateColumn, GuildHistoryId

if TYPE_CHECKING:
    from src import GuildResponse


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
        datetime: DateColumn
    ) -> None:
        self._name = name
        self._level = level
        self._territories = territories
        self._wars = wars
        self._member_total = member_total
        self._online_members = online_members
        self._datetime = datetime

    @classmethod
    def from_responses(cls, resps: Iterable[GuildResponse]) -> tuple[GuildHistory, ...]:
        return tuple(cls(
            name=resp.body.name,
            level=Decimal(resp.body.level),
            territories=resp.body.territories,
            wars=resp.body.wars,
            member_total=resp.body.members.total,
            online_members=resp.body.members.get_online_members(),
            datetime=DateColumn(resp.get_datetime())
        ) for resp in resps)

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
    def datetime(self) -> DateColumn:
        return self._datetime
