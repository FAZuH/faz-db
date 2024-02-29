from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

from . import Repository
from ..model import GuildInfo, GuildInfoId

if TYPE_CHECKING:
    from aiomysql import Connection
    from kans.db import DatabaseQuery
    from kans.util import DbModelDictAdapter, DbModelIdDictAdapter



class GuildInfoRepository(Repository[GuildInfo, GuildInfoId]):

    _TABLE_NAME = "guild_info"

    def __init__(
        self,
        db: DatabaseQuery,
        db_model_dict_adapter: DbModelDictAdapter,
        db_model_id_dict_adapter: DbModelIdDictAdapter
    ) -> None:
        super().__init__(db)
        self._adapt = db_model_dict_adapter.from_guild_info
        self._adapt_id = db_model_id_dict_adapter.from_guild_info

    async def insert(self, entities: Iterable[GuildInfo], conn: None | Connection = None) -> int:
        # NOTE: This doesn't change. Ignore duplicates.
        SQL = f"""
            INSERT IGNORE INTO `{self.table_name}` (`name`, `prefix`, `created`)
            VALUES (%(name)s, %(prefix)s, %(created)s)
        """
        return await self._db.execute_many(SQL, tuple(self._adapt(entity) for entity in entities), conn)

    async def exists(self, id_: GuildInfoId, conn: None | Connection = None) -> bool:
        SQL = f"SELECT COUNT(*) AS count FROM `{self.table_name}` WHERE `name` = %(name)s"
        result = await self._db.fetch(SQL, self._adapt_id(id_), connection=conn)
        return result[0].get("count", 0) > 0

    async def count(self, conn: None | Connection = None) -> float:
        SQL = f"SELECT COUNT(*) FROM `{self.table_name}`"
        return (await self._db.fetch(SQL, connection=conn))[0].get("COUNT(*)", 0)

    async def find_one(self, id_: GuildInfoId, conn: None | Connection = None) -> None | GuildInfo:
        SQL = f"SELECT * FROM `{self.table_name}` WHERE `name` = %(name)s"
        result = await self._db.fetch(SQL, self._adapt_id(id_), connection=conn)
        return GuildInfo(**result[0]) if result else None

    async def find_all(self, conn: None | Connection = None) -> list[GuildInfo]:
        SQL = f"SELECT * FROM `{self.table_name}`"
        result = await self._db.fetch(SQL, connection=conn)
        return [GuildInfo(**row) for row in result] if result else []

    async def update(self, entities: Iterable[GuildInfo], conn: None | Connection = None) -> int:
        SQL = f"""
            UPDATE `{self.table_name}`
            SET `prefix` = %(prefix)s
            WHERE `name` = %(name)s
        """
        return await self._db.execute_many(SQL, tuple(self._adapt(entity) for entity in entities), conn)

    async def delete(self, id_: GuildInfoId, conn: None | Connection = None) -> int:
        SQL = f"DELETE FROM `{self.table_name}` WHERE `name` = %(name)s"
        return await self._db.execute(SQL, self._adapt_id(id_), conn)

    async def create_table(self, conn: None | Connection = None) -> None:
        SQL = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                `name` varchar(30) NOT NULL,
                `prefix` varchar(4) NOT NULL,
                `created` datetime NOT NULL,
                PRIMARY KEY (`name`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(SQL)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
