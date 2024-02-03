from __future__ import annotations
from typing import TYPE_CHECKING, Iterable
from typing_extensions import override

from src import DateColumn, PlayerInfoId, UuidColumn

if TYPE_CHECKING:
    from src import PlayerResponse


class PlayerInfo(PlayerInfoId):
    """implements `PlayerInfoId`

    id: `uuid`"""

    def __init__(self, uuid: UuidColumn, latest_username: str, first_join: DateColumn) -> None:
        self._uuid = uuid
        self._latest_username = latest_username
        self._first_join = first_join

    @classmethod
    def from_responses(cls, resps: Iterable[PlayerResponse]) -> tuple[PlayerInfo, ...]:
        return tuple(cls(
            uuid=UuidColumn(resp.body.uuid.to_bytes()),
            latest_username=resp.body.username,
            first_join=DateColumn(resp.body.first_join.to_datetime())
        ) for resp in resps)

    @property
    @override
    def uuid(self) -> UuidColumn:
        return self._uuid

    @property
    def latest_username(self) -> str:
        return self._latest_username

    @property
    def first_join(self) -> DateColumn:
        return self._first_join
