from . import CharacterInfoId
from .. import UuidColumn


class CharacterInfo(CharacterInfoId):
    """implements ``CharacterInfoId``

    id: `character_uuid`"""

    def __init__(self, character_uuid: bytes | UuidColumn, uuid: bytes | UuidColumn, type: str) -> None:
        super().__init__(character_uuid)
        self._uuid = uuid if isinstance(uuid, UuidColumn) else UuidColumn(uuid)
        self._type = type

    @property
    def uuid(self) -> UuidColumn:
        return self._uuid

    @property
    def type(self) -> str:
        return self._type
