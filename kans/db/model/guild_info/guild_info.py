from __future__ import annotations
from typing import TYPE_CHECKING, Iterable
from typing_extensions import override

from kans import DateColumn, GuildInfoId

if TYPE_CHECKING:
    from kans import GuildResponse


class GuildInfo(GuildInfoId):
    """implements `GuildInfoId`

    id: `name`"""

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
    def from_responses(cls, resps: Iterable[GuildResponse]) -> tuple[GuildInfo, ...]:
        return tuple(cls(
            name=resp.body.name,
            prefix=resp.body.prefix,
            created=DateColumn(resp.body.created.to_datetime())
        ) for resp in resps)

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
