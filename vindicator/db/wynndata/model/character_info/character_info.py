from __future__ import annotations
from typing import TYPE_CHECKING, Self
from typing_extensions import override

from vindicator import CharacterInfoId, UuidColumn

if TYPE_CHECKING:
    from vindicator import PlayerResponse


class CharacterInfo(CharacterInfoId):
    """id: character_uuid"""

    def __init__(self, character_uuid: UuidColumn, uuid: UuidColumn, type: str) -> None:
        self._character_uuid = character_uuid
        self._uuid = uuid
        self._type = type

    @classmethod
    def from_response(cls, response: PlayerResponse) -> list[Self]:
        return [
            cls(
                character_uuid=UuidColumn(character_uuid.to_bytes()),
                uuid=UuidColumn(response.body.uuid.to_bytes()),
                type=character.type.get_kind()
            ) for character_uuid, character in response.body.iter_characters()
        ]

    @property
    @override
    def character_uuid(self) -> UuidColumn:
        return self._character_uuid

    @property
    def uuid(self) -> UuidColumn:
        return self._uuid

    @property
    def type(self) -> str:
        return self._type
