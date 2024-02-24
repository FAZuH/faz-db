from __future__ import annotations
from typing import TYPE_CHECKING
from .. import DateColumn, UuidColumn

if TYPE_CHECKING:
    from datetime import datetime as dt


class CharacterHistoryId:

    def __init__(self, character_uuid: bytes | UuidColumn, datetime: dt | DateColumn) -> None:
        self._character_uuid = character_uuid if isinstance(character_uuid, UuidColumn) else UuidColumn(character_uuid)
        self._datetime = datetime if isinstance(datetime, DateColumn) else DateColumn(datetime)

    @property
    def character_uuid(self) -> UuidColumn:
        return self._character_uuid

    @property
    def datetime(self) -> DateColumn:
        return self._datetime
