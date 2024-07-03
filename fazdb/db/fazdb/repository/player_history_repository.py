from __future__ import annotations
from typing import TYPE_CHECKING, Any

from ..model import PlayerHistory
from ._repository import Repository

if TYPE_CHECKING:
    from ... import BaseAsyncDatabase


class PlayerHistoryRepository(Repository[PlayerHistory, Any]):

    def __init__(self, database: BaseAsyncDatabase[Any]) -> None:
        super().__init__(database, PlayerHistory)
