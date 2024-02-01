from __future__ import annotations
from typing import TYPE_CHECKING
from typing_extensions import override

from vindicator import PlayerInfoId, UuidColumn

if TYPE_CHECKING:
    from datetime import datetime as dt
    from vindicator import PlayerResponse


class PlayerInfo(PlayerInfoId):
    """id: uuid"""

    def __init__(self, uuid: UuidColumn, latest_username: str, first_join: dt) -> None:
        self._uuid = uuid
        self._latest_username = latest_username
        self._first_join = first_join

    @classmethod
    def from_model(cls, response: PlayerResponse) -> PlayerInfo:
        return cls(
            uuid=UuidColumn(response.body.uuid.to_bytes()),
            latest_username=response.body.username,
            first_join=response.body.first_join.to_datetime()
        )

    @property
    @override
    def uuid(self) -> UuidColumn:
        return self._uuid

    @property
    def latest_username(self) -> str:
        return self._latest_username

    @property
    def first_join(self) -> dt:
        return self._first_join
