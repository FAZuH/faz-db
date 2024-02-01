from __future__ import annotations
from typing import TYPE_CHECKING, Self
from typing_extensions import override

from vindicator import DateColumn, GuildMemberHistoryId, UuidColumn

if TYPE_CHECKING:
    from vindicator import GuildResponse


class GuildMemberHistory(GuildMemberHistoryId):
    """id: uuid, datetime"""

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
    def from_response(cls, response: GuildResponse) -> list[Self]:
        return [
            cls(
                uuid=UuidColumn(uuid.to_bytes() if uuid.is_uuid() else memberinfo.uuid.to_bytes()),  # type: ignore
                contributed=memberinfo.contributed,
                joined=DateColumn(memberinfo.joined.to_datetime()),
                datetime=DateColumn(response.get_datetime())
            ) for rank, uuid, memberinfo in response.body.members.iter_online_members()  # type: ignore
        ]

    @property
    @override
    def uuid(self) -> UuidColumn:
        return self._uuid

    @property
    def contributed(self) -> int:
        return self._contributed

    @property
    def joined(self) -> DateColumn:
        return self._joined

    @property
    @override
    def datetime(self) -> DateColumn:
        return self._datetime
