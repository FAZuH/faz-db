from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from src import DateColumn, UuidColumn


class GuildMemberHistoryId(Protocol):
    @property
    def uuid(self) -> UuidColumn: ...
    @property
    def datetime(self) -> DateColumn: ...
