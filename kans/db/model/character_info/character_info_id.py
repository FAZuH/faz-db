from ..uuid_column import UuidColumn


class CharacterInfoId:

    def __init__(self, character_uuid: bytes | UuidColumn) -> None:
        self._character_uuid: UuidColumn = character_uuid if isinstance(character_uuid, UuidColumn) else UuidColumn(character_uuid)

    @property
    def character_uuid(self) -> UuidColumn:
        return self._character_uuid
