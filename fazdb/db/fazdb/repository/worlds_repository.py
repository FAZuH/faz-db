from __future__ import annotations
from typing import TYPE_CHECKING, Any, Iterable

from ..model import Worlds
from ._repository import Repository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from ... import BaseAsyncDatabase


class WorldsRepository(Repository[Worlds, Any]):

    def __init__(self, database: BaseAsyncDatabase[Any]) -> None:
        super().__init__(database, Worlds)

    async def update_worlds(self, entity: Iterable[Worlds], *, session: AsyncSession | None = None) -> None:
        """Deletes worlds that's not up anymore, and updates player_count for worlds that's still up"""
        stmt = self.table.delete().where(self.model.name.not_in([e.name for e in entity]))
        async with self.database.enter_session() as session:
            await session.execute(stmt)
            await self.insert(entity, session=session, replace_on_duplicate=True, columns_to_replace=["player_count"])
