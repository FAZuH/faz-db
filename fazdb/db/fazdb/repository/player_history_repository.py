from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ...base_repository import BaseRepository
from ..model import PlayerHistory

if TYPE_CHECKING:
    from ...base_async_database import BaseAsyncDatabase


class PlayerHistoryRepository(BaseRepository[PlayerHistory, Any]):

    def __init__(self, database: BaseAsyncDatabase[Any]) -> None:
        super().__init__(database, PlayerHistory)
