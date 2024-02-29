from __future__ import annotations
from typing import TypedDict

from . import CharacterInfoId


class CharacterInfo(CharacterInfoId):
    """implements ``CharacterInfoId``

    id: `character_uuid`"""

    def __init__(self, character_uuid: str, uuid: str, type: str) -> None:
        super().__init__(character_uuid)
        self._uuid = uuid
        self._type = type

    class Type(TypedDict):
        character_uuid: str
        uuid: str
        type: str

    @property
    def uuid(self) -> str:
        return self._uuid

    @property
    def type(self) -> str:
        return self._type
