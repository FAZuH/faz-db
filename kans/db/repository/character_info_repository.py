from __future__ import annotations
from typing import TYPE_CHECKING, Any, Iterable

from kans import CharacterInfo, Repository

if TYPE_CHECKING:
    from aiomysql import Connection
    from kans import DatabaseQuery


class CharacterInfoRepository(Repository[CharacterInfo]):

    _TABLE_NAME: str = "character_info"

    def __init__(self, db: DatabaseQuery) -> None:
        self._db = db

    async def insert(self, entities: Iterable[CharacterInfo], conn: None | Connection = None) -> int:
        # NOTE: This doesn't change. Ignore duplicates.
        sql = f"""
            INSERT IGNORE INTO `{self.table_name}` (`character_uuid`, `type`, `uuid`)
            VALUES (%s, %s, %s)
        """
        return await self._db.execute_many(
                sql,
                tuple((
                        entity.character_uuid.uuid,
                        entity.type,
                        entity.uuid)
                        for entity in entities
                ),
                conn
        )

    async def exists(self, id_: Any, conn: None | Connection = None) -> bool: ...

    async def count(self, conn: None | Connection = None) -> float:
        sql = f"SELECT COUNT(*) FROM `{self.table_name}`"
        return (await self._db.fetch(sql, connection=conn))[0].get("COUNT(*)", 0)

    async def find_one(self, id_: Any, conn: None | Connection = None) -> None | CharacterInfo: ...

    async def find_all(self, conn: None | Connection = None) -> None | list[CharacterInfo]: ...

    async def update(self, entities: Iterable[CharacterInfo], conn: None | Connection = None) -> int: ...

    async def delete(self, id_: Any, conn: None | Connection = None) -> int: ...

    async def create_table(self, conn: None | Connection = None) -> None:
        sql = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                `character_uuid` binary(16) NOT NULL,
                `uuid` binary(16) NOT NULL,
                `type` enum('ARCHER','ASSASSIN','MAGE','SHAMAN','WARRIOR') NOT NULL,
                PRIMARY KEY (`character_uuid`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(sql)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
