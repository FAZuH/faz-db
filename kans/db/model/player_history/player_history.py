from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from . import PlayerHistoryId

if TYPE_CHECKING:
    from .. import DateColumn, UuidColumn
    from datetime import datetime as dt


class PlayerHistory(PlayerHistoryId):
    """implements `PlayerHistoryId`

    id: `uuid`, `datetime`"""

    def __init__(
        self,
        uuid: bytes | UuidColumn,
        username: str,
        support_rank: None | str,
        playtime: Decimal,
        guild_name: None | str,
        guild_rank: None | str,
        rank: None | str,
        datetime: dt | DateColumn
    ) -> None:
        super().__init__(uuid, datetime)
        self._username = username
        self._support_rank = support_rank
        self._playtime = playtime
        self._guild_name = guild_name
        self._guild_rank = guild_rank
        self._rank = rank

    def to_dict(self) -> dict[str, Any]:
        return {
                "uuid": self.uuid.uuid,
                "username": self.username,
                "support_rank": self.support_rank,
                "playtime": self.playtime,
                "guild_name": self.guild_name,
                "guild_rank": self.guild_rank,
                "rank": self.rank,
                "datetime": self.datetime.datetime
        }

    @property
    def username(self) -> str:
        return self._username

    @property
    def support_rank(self) -> None | str:
        return self._support_rank

    @property
    def playtime(self) -> Decimal:
        return self._playtime

    @property
    def guild_name(self) -> None | str:
        return self._guild_name

    @property
    def guild_rank(self) -> None | str:
        return self._guild_rank

    @property
    def rank(self) -> None | str:
        return self._rank
