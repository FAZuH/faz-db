from __future__ import annotations
from typing import TYPE_CHECKING
from typing_extensions import override

from vindicator import DateColumn, GuildInfoId

if TYPE_CHECKING:
    from vindicator import GuildResponse


class GuildInfo(GuildInfoId):
    """id: name"""

    def __init__(
        self,
        name: str,
        prefix: str,
        created: DateColumn
    ) -> None:
        self._name = name
        self._prefix = prefix
        self._created = created

    @classmethod
    def from_response(cls, response: GuildResponse) -> GuildInfo:
        return cls(
            name=response.body.name,
            prefix=response.body.prefix,
            created=DateColumn(response.body.created.to_datetime())
        )

    @property
    @override
    def name(self) -> str:
        return self._name

    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def created(self) -> DateColumn:
        return self._created
