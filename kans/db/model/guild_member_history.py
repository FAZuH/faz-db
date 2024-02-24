from __future__ import annotations
from typing import TYPE_CHECKING, Iterable, Self


from kans import DateColumn, UuidColumn

if TYPE_CHECKING:
    from kans import GuildResponse


class GuildMemberHistory:
    """implements `GuildMemberHistoryId`

    id: `uuid`, `datetime`"""

    def __init__(
        self,
        uuid: UuidColumn,
        contributed: int,
        joined: DateColumn,
        datetime: DateColumn
    ) -> None:
        self._uuid = uuid
        self._contributed = contributed
        self._joined = joined
        self._datetime = datetime

    @classmethod
    def from_responses(cls, resps: Iterable[GuildResponse]) -> tuple[Self]:
        return tuple(cls(
            uuid=UuidColumn(uuid.to_bytes() if uuid.is_uuid() else memberinfo.uuid.to_bytes()),  # type: ignore
            contributed=memberinfo.contributed,
            joined=DateColumn(memberinfo.joined.to_datetime()),
            datetime=DateColumn(resp.get_datetime())
        ) for resp in resps for rank, uuid, memberinfo in resp.body.members.iter_online_members())  # type: ignore

    @property
    def uuid(self) -> UuidColumn:
        return self._uuid

    @property
    def contributed(self) -> int:
        return self._contributed

    @property
    def joined(self) -> DateColumn:
        return self._joined

    @property
    def datetime(self) -> DateColumn:
        return self._datetime