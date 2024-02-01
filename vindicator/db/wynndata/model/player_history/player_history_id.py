from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from datetime import datetime as dt
    from vindicator import UuidColumn


class PlayerHistoryId(Protocol):
    @property
    def uuid(self) -> UuidColumn: ...
    @property
    def datetime(self) -> dt: ...
