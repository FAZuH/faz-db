from __future__ import annotations
from typing import TYPE_CHECKING, Any

from . import GuildInfoId
from .. import DateColumn

if TYPE_CHECKING:
    from datetime import datetime as dt


class GuildInfo(GuildInfoId):
    """implements `GuildInfoId`

    id: `name`"""

    def __init__(
        self,
        name: str,
        prefix: str,
        created: dt | DateColumn
    ) -> None:
        super().__init__(name)
        self._prefix = prefix
        self._created = created if isinstance(created, DateColumn) else DateColumn(created)

    def to_tuple(self) -> tuple[Any, ...]:
        return (self.name, self.prefix, self.created.datetime)

    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def created(self) -> DateColumn:
        return self._created
