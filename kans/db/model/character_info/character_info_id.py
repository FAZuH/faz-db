from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from kans import UuidColumn


class CharacterInfoId(Protocol):
    @property
    def character_uuid(self) -> UuidColumn: ...
