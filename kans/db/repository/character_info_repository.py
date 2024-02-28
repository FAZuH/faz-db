from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

from . import Repository
from ..model import CharacterInfo, CharacterInfoId

if TYPE_CHECKING:
    from aiomysql import Connection


class CharacterInfoRepository(Repository[CharacterInfo, CharacterInfoId]):

    _TABLE_NAME: str = "character_info"

    async def insert(self, entities: Iterable[CharacterInfo], conn: None | Connection = None) -> int:
        # NOTE: This doesn't change. Ignore duplicates.
        SQL = f"""
            INSERT IGNORE INTO `{self.table_name}` (`character_uuid`, `uuid`, `type`)
            VALUES (%s, %s, %s)
        """
        return await self._db.execute_many(SQL, tuple(entity.to_tuple() for entity in entities), conn)

    async def exists(self, id_: CharacterInfoId, conn: None | Connection = None) -> bool: ...

    async def count(self, conn: None | Connection = None) -> float:
        SQL = f"SELECT COUNT(*) FROM `{self.table_name}`"
        result = await self._db.fetch(SQL, connection=conn)
        return result[0].get("COUNT(*)", 0)

    async def find_one(self, id_: CharacterInfoId, conn: None | Connection = None) -> None | CharacterInfo: ...

    async def find_all(self, conn: None | Connection = None) -> None | list[CharacterInfo]: ...

    async def update(self, entities: Iterable[CharacterInfo], conn: None | Connection = None) -> int: ...

    async def delete(self, id_: CharacterInfoId, conn: None | Connection = None) -> int: ...

    async def create_table(self, conn: None | Connection = None) -> None:
        SQL = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                `character_uuid` binary(16) NOT NULL,
                `uuid` binary(16) NOT NULL,
                `type` enum('ARCHER','ASSASSIN','MAGE','SHAMAN','WARRIOR') NOT NULL,
                PRIMARY KEY (`character_uuid`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(SQL)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
