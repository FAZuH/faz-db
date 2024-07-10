from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ...base_repository import BaseRepository
from ..model import OnlinePlayers

if TYPE_CHECKING:
    from ...base_async_database import BaseAsyncDatabase


class OnlinePlayersRepository(BaseRepository[OnlinePlayers, Any]):

    def __init__(self, database: BaseAsyncDatabase[Any]) -> None:
        super().__init__(database, OnlinePlayers)
