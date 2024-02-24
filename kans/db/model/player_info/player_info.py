from __future__ import annotations
from typing import TYPE_CHECKING

from . import PlayerInfoId
from .. import DateColumn

if TYPE_CHECKING:
    from datetime import datetime as dt
    from .. import UuidColumn


class PlayerInfo(PlayerInfoId):
    """implements `PlayerInfoId`

    id: `uuid`"""

    def __init__(self, uuid: bytes | UuidColumn, latest_username: str, first_join: dt | DateColumn) -> None:
        super().__init__(uuid)
        self._latest_username = latest_username
        self._first_join = first_join if isinstance(first_join, DateColumn) else DateColumn(first_join)

    @property
    def latest_username(self) -> str:
        return self._latest_username

    @property
    def first_join(self) -> DateColumn:
        return self._first_join