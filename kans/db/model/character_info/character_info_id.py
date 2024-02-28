from __future__ import annotations
from typing import TypedDict

from ..uuid_column import UuidColumn


class CharacterInfoId:

    def __init__(self, character_uuid: bytes | UuidColumn) -> None:
        self._character_uuid: UuidColumn = character_uuid if isinstance(character_uuid, UuidColumn) else UuidColumn(character_uuid)

    def to_dict(self) -> CharacterInfoId.Type:
        return {
                "character_uuid": self.character_uuid.uuid
        }

    class Type(TypedDict):
        character_uuid: bytes

    @property
    def character_uuid(self) -> UuidColumn:
        return self._character_uuid
