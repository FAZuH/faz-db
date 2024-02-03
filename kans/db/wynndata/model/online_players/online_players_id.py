from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from src import UuidColumn


class OnlinePlayersId(Protocol):
    @property
    def uuid(self) -> UuidColumn: ...
