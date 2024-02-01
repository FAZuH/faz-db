from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from vindicator import UuidColumn


class OnlinePlayersId(Protocol):
    @property
    def uuid(self) -> UuidColumn: ...
