from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

from . import GuildInfoId
from .. import DateColumn

if TYPE_CHECKING:
    from datetime import datetime


class GuildInfo(GuildInfoId):
    """implements `GuildInfoId`

    id: `name`"""

    def __init__(
        self,
        name: str,
        prefix: str,
        created: datetime | DateColumn
    ) -> None:
        super().__init__(name)
        self._prefix = prefix
        self._created = created if isinstance(created, DateColumn) else DateColumn(created)

    def to_dict(self) -> GuildInfo.Type:
        return {
                "name": self.name,
                "prefix": self.prefix,
                "created": self.created.datetime
        }

    class Type(TypedDict):
        name: str
        prefix: str
        created: datetime

    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def created(self) -> DateColumn:
        return self._created
