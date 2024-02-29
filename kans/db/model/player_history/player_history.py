from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING, TypedDict

from . import PlayerHistoryId

if TYPE_CHECKING:
    from .. import DateColumn
    from datetime import datetime


class PlayerHistory(PlayerHistoryId):
    """implements `PlayerHistoryId`

    id: `uuid`, `datetime`"""

    def __init__(
        self,
        uuid: str,
        username: str,
        support_rank: None | str,
        playtime: Decimal,
        guild_name: None | str,
        guild_rank: None | str,
        rank: None | str,
        datetime: datetime | DateColumn
    ) -> None:
        super().__init__(uuid, datetime)
        self._username = username
        self._support_rank = support_rank
        self._playtime = playtime
        self._guild_name = guild_name
        self._guild_rank = guild_rank
        self._rank = rank

    class Type(TypedDict):
        uuid: str
        username: str
        support_rank: None | str
        playtime: Decimal
        guild_name: None | str
        guild_rank: None | str
        rank: None | str
        datetime: datetime

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
