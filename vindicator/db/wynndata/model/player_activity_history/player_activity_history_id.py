from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from vindicator import DateColumn, UuidColumn


class PlayerActivityHistoryId(Protocol):
    @property
    def uuid(self) -> UuidColumn: ...
    @property
    def logon_datetime(self) -> DateColumn: ...
