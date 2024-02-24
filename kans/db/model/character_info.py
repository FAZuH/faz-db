from __future__ import annotations
from typing import TYPE_CHECKING, Iterable, Self


from kans import UuidColumn

if TYPE_CHECKING:
    from kans import PlayerResponse


class CharacterInfo:
    """implements ``CharacterInfoId``

    id: `character_uuid`"""

    def __init__(self, character_uuid: UuidColumn, uuid: UuidColumn, type: str) -> None:
        self._character_uuid = character_uuid
        self._uuid = uuid
        self._type = type

    @classmethod
    def from_responses(cls, resps: Iterable[PlayerResponse]) -> tuple[Self, ...]:
        return tuple(cls(
                character_uuid=UuidColumn(character_uuid.to_bytes()),
                uuid=UuidColumn(resp.body.uuid.to_bytes()),
                type=character.type.get_kind()
            ) for resp in resps for character_uuid, character in resp.body.iter_characters()
        )

    @property
    def character_uuid(self) -> UuidColumn:
        return self._character_uuid

    @property
    def uuid(self) -> UuidColumn:
        return self._uuid

    @property
    def type(self) -> str:
        return self._type
