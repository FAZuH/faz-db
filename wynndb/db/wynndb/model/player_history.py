from __future__ import annotations
from decimal import Decimal
import hashlib
from typing import TYPE_CHECKING, TypedDict

from . import DateColumn, UuidColumn

if TYPE_CHECKING:
    from datetime import datetime


class PlayerHistory:

    def __init__(
        self,
        uuid: bytes | UuidColumn,
        username: str,
        support_rank: None | str,
        playtime: Decimal,
        guild_name: None | str,
        guild_rank: None | str,
        rank: None | str,
        datetime: datetime | DateColumn,
    ) -> None:
        self._uuid = uuid if isinstance(uuid, UuidColumn) else UuidColumn(uuid)
        self._datetime = datetime if isinstance(datetime, DateColumn) else DateColumn(datetime)
        self._username = username
        self._support_rank = support_rank
        self._playtime = playtime
        self._guild_name = guild_name
        self._guild_rank = guild_rank
        self._rank = rank
        self._unique_id = UuidColumn(hashlib.sha256(f"{uuid}{username}{support_rank}{guild_name}{guild_rank}{rank}".encode()).digest())

    @property
    def uuid(self) -> UuidColumn:
        return self._uuid

    @property
    def datetime(self) -> DateColumn:
        return self._datetime

    @property
    def unique_id(self) -> UuidColumn:
        return self._unique_id

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

    class Type(TypedDict):
        uuid: bytes
        username: str
        support_rank: None | str
        playtime: Decimal
        guild_name: None | str
        guild_rank: None | str
        rank: None | str
        datetime: datetime
        unique_id: bytes