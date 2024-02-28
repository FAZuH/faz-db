from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

from .. import DateColumn, UuidColumn

if TYPE_CHECKING:
    from datetime import datetime


class CharacterHistoryId:

    def __init__(self, character_uuid: bytes | UuidColumn, datetime: datetime | DateColumn) -> None:
        self._character_uuid = character_uuid if isinstance(character_uuid, UuidColumn) else UuidColumn(character_uuid)
        self._datetime = datetime if isinstance(datetime, DateColumn) else DateColumn(datetime)

    def to_dict(self) -> CharacterHistoryId.Type:
        return {
                "character_uuid": self.character_uuid.uuid,
                "datetime": self.datetime.datetime
        }

    class Type(TypedDict):
        character_uuid: bytes
        datetime: datetime

    @property
    def character_uuid(self) -> UuidColumn:
        return self._character_uuid

    @property
    def datetime(self) -> DateColumn:
        return self._datetime
