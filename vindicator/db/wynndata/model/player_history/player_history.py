from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING
from typing_extensions import override

from vindicator import DateColumn, PlayerHistoryId, UuidColumn

if TYPE_CHECKING:
    from vindicator import PlayerResponse


class PlayerHistory(PlayerHistoryId):
    """id: uuid, datetime"""

    def __init__(
        self,
        uuid: UuidColumn,
        username: str,
        support_rank: None | str,
        playtime: Decimal,
        guild_name: None | str,
        guild_rank: None | str,
        rank: None | str,
        datetime: DateColumn
    ) -> None:
        self._uuid = uuid
        self._username = username
        self._support_rank = support_rank
        self._playtime = playtime
        self._guild_name = guild_name
        self._guild_rank = guild_rank
        self._rank = rank
        self._datetime = datetime

    @classmethod
    def from_response(cls, response: PlayerResponse) -> PlayerHistory:
        return cls(
            uuid=UuidColumn(response.body.uuid.to_bytes()),
            username=response.body.username,
            support_rank=response.body.support_rank,
            playtime=Decimal(response.body.playtime),
            guild_name=response.body.guild.name if response.body.guild else None,
            guild_rank=response.body.guild.name if response.body.guild else None,
            rank=response.body.rank,
            datetime=DateColumn(response.get_datetime())
        )

    @property
    @override
    def uuid(self) -> UuidColumn:
        return self._uuid

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

    @property
    @override
    def datetime(self) -> DateColumn:
        return self._datetime
