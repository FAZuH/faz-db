from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING, Iterable


from kans import DateColumn, UuidColumn

if TYPE_CHECKING:
    from kans import PlayerResponse


class PlayerHistory:
    """implements `PlayerHistoryId`

    id: `uuid`, `datetime`"""

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
    def from_responses(cls, resps: Iterable[PlayerResponse]) -> tuple[PlayerHistory, ...]:
        return tuple(cls(
            uuid=UuidColumn(resp.body.uuid.to_bytes()),
            username=resp.body.username,
            support_rank=resp.body.support_rank,
            playtime=Decimal(resp.body.playtime),
            guild_name=resp.body.guild.name if resp.body.guild else None,
            guild_rank=resp.body.guild.rank if resp.body.guild else None,
            rank=resp.body.rank,
            datetime=DateColumn(resp.get_datetime())
        ) for resp in resps)

    @property
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
    def datetime(self) -> DateColumn:
        return self._datetime
