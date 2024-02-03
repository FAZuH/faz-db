from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from kans import DateColumn


class GuildHistoryId(Protocol):
    @property
    def name(self) -> str: ...
    @property
    def datetime(self) -> DateColumn: ...
