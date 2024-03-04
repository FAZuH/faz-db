from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

from kans.db.kans.model.uuid_column import UuidColumn

from . import GuildInfoId
from .. import DateColumn

if TYPE_CHECKING:
    from datetime import datetime


class GuildInfo(GuildInfoId):
    """implements `GuildInfoId`

    id: `name`"""

    def __init__(
        self,
        uuid: bytes | UuidColumn,
        name: str,
        prefix: str,
        created: datetime | DateColumn
    ) -> None:
        super().__init__(name)
        self._uuid = uuid if isinstance(uuid, UuidColumn) else UuidColumn(uuid)
        self._prefix = prefix
        self._created = created if isinstance(created, DateColumn) else DateColumn(created)

    class Type(TypedDict):
        uuid: bytes
        name: str
        prefix: str
        created: datetime

    @property
    def uuid(self) -> UuidColumn:
        return self._uuid

    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def created(self) -> DateColumn:
        return self._created
