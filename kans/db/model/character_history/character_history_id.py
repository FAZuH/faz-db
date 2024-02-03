from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from kans import DateColumn, UuidColumn


class CharacterHistoryId(Protocol):
    @property
    def character_uuid(self) -> UuidColumn: ...
    @property
    def datetime(self) -> DateColumn: ...
