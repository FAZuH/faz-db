from __future__ import annotations
from typing import TypedDict


class CharacterInfoId:

    def __init__(self, character_uuid: str) -> None:
        self._character_uuid: str = character_uuid

    class IdType(TypedDict):
        character_uuid: str

    @property
    def character_uuid(self) -> str:
        return self._character_uuid
