from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

from .. import DateColumn

if TYPE_CHECKING:
    from datetime import datetime


class CharacterHistoryId:

    def __init__(self, character_uuid: str, datetime: datetime | DateColumn) -> None:
        self._character_uuid = character_uuid
        self._datetime = datetime if isinstance(datetime, DateColumn) else DateColumn(datetime)

    class IdType(TypedDict):
        character_uuid: str
        datetime: datetime

    @property
    def character_uuid(self) -> str:
        return self._character_uuid

    @property
    def datetime(self) -> DateColumn:
        return self._datetime
