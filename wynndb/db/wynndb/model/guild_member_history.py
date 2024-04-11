from __future__ import annotations
import hashlib
from typing import TYPE_CHECKING, TypedDict

from . import DateColumn, UuidColumn

if TYPE_CHECKING:
    from datetime import datetime


class GuildMemberHistory:

    def __init__(
        self,
        uuid: bytes | UuidColumn,
        contributed: int,
        joined: datetime | DateColumn,
        datetime: datetime | DateColumn,
    ) -> None:
        self._uuid = uuid if isinstance(uuid, UuidColumn) else UuidColumn(uuid)
        self._datetime = datetime if isinstance(datetime, DateColumn) else DateColumn(datetime)
        self._contributed = contributed
        self._joined = joined if isinstance(joined, DateColumn) else DateColumn(joined)
        self._unique_id = UuidColumn(hashlib.sha256(f"{uuid}{contributed}{joined}".encode()).digest())

    @property
    def uuid(self) -> UuidColumn:
        return self._uuid

    @property
    def datetime(self) -> DateColumn:
        return self._datetime

    @property
    def unique_id(self) -> UuidColumn:
        return self._unique_id

    @property
    def contributed(self) -> int:
        return self._contributed

    @property
    def joined(self) -> DateColumn:
        return self._joined

    class Type(TypedDict):
        uuid: bytes
        contributed: int
        joined: datetime
        datetime: datetime
        unique_id: bytes
