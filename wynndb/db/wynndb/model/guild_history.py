from __future__ import annotations
from decimal import Decimal
import hashlib
from typing import TYPE_CHECKING, TypedDict

from . import DateColumn, UuidColumn

if TYPE_CHECKING:
    from datetime import datetime


class GuildHistory:

    def __init__(
        self,
        name: str,
        level: Decimal,
        territories: int,
        wars: int,
        member_total: int,
        online_members: int,
        datetime: datetime | DateColumn,
    ) -> None:
        self._name = name
        self._datetime = datetime if isinstance(datetime, DateColumn) else DateColumn(datetime)
        self._level = level
        self._territories = territories
        self._wars = wars
        self._member_total = member_total
        self._online_members = online_members
        self._unique_id = UuidColumn(hashlib.sha256(f"{name}{level}{territories}{wars}{member_total}{online_members}".encode()).digest())

    @property
    def name(self) -> str:
        return self._name

    @property
    def datetime(self) -> DateColumn:
        return self._datetime

    @property
    def unique_id(self) -> UuidColumn:
        return self._unique_id

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

    class Type(TypedDict):
        name: str
        level: Decimal
        territories: int
        wars: int
        member_total: int
        online_members: int
        datetime: datetime
        unique_id: bytes
