from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ...base_repository import BaseRepository
from ..model import PlayerActivityHistory

if TYPE_CHECKING:
    from ...base_async_database import BaseAsyncDatabase


class PlayerActivityHistoryRepository(BaseRepository[PlayerActivityHistory, Any]):

    def __init__(self, database: BaseAsyncDatabase[Any]) -> None:
        super().__init__(database, PlayerActivityHistory)
