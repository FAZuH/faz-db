from typing import TypedDict


class PlayerCharacter(TypedDict):
    character_uuid: bytes  # NOTE: binary(16)
    type: str  # NOTE: enum('ARCHER', 'ASSASSIN', 'MAGE', 'SHAMAN', 'WARRIOR')
    uuid: bytes  # NOTE: binary(16)
