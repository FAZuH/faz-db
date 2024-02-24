from __future__ import annotations
from typing import TYPE_CHECKING

from kans import DateColumn

if TYPE_CHECKING:
    from datetime import datetime as dt


class GuildInfo:
    """implements `GuildInfoId`

    id: `name`"""

    def __init__(
        self,
        name: str,
        prefix: str,
        created: dt | DateColumn
    ) -> None:
        self._name = name
        self._prefix = prefix
        self._created = created if isinstance(created, DateColumn) else DateColumn(created)

    @property
    def name(self) -> str:
        return self._name

    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def created(self) -> DateColumn:
        return self._created
