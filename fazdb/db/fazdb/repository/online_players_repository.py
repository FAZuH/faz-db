from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ..model import OnlinePlayers
from ._repository import Repository

if TYPE_CHECKING:
    from ... import BaseAsyncDatabase


class OnlinePlayersRepository(Repository[OnlinePlayers, Any]):

    def __init__(self, database: BaseAsyncDatabase[Any]) -> None:
        super().__init__(database, OnlinePlayers)
