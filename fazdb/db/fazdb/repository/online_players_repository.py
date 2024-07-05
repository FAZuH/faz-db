from __future__ import annotations
from typing import Any, TYPE_CHECKING, Iterable

from ..model import OnlinePlayers
from ._repository import Repository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from ... import BaseAsyncDatabase


class OnlinePlayersRepository(Repository[OnlinePlayers, Any]):

    def __init__(self, database: BaseAsyncDatabase[Any]) -> None:
        super().__init__(database, OnlinePlayers)

    async def insert_new_online_players(self, entities: Iterable[OnlinePlayers], session: AsyncSession | None = None) -> None:
        async with self.database.must_enter_session(session) as session:
            await self.truncate(session)
            await self.insert(entities, session, replace_on_duplicate=True)
