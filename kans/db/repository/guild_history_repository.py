from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

from . import Repository
from ..model import GuildHistory, GuildHistoryId

if TYPE_CHECKING:
    from aiomysql import Connection
    from kans.db import DatabaseQuery
    from kans.util import DbModelDictAdapter, DbModelIdDictAdapter



class GuildHistoryRepository(Repository[GuildHistory, GuildHistoryId]):

    _TABLE_NAME: str = "guild_history"

    def __init__(
        self,
        db: DatabaseQuery,
        db_model_dict_adapter: DbModelDictAdapter,
        db_model_id_dict_adapter: DbModelIdDictAdapter
    ) -> None:
        super().__init__(db)
        self._adapt = db_model_dict_adapter.from_guild_history
        self._adapt_id = db_model_id_dict_adapter.from_guild_history

    async def insert(self, entities: Iterable[GuildHistory], conn: None | Connection = None) -> int:
        SQL = f"""
            INSERT IGNORE INTO `{self.table_name}`
                (`name`, `level`, `territories`, `wars`, `member_total`, `online_members`, `datetime`)
            VALUES (%(name)s, %(level)s, %(territories)s, %(wars)s, %(member_total)s, %(online_members)s, %(datetime)s)
        """
        return await self._db.execute_many(SQL, tuple(self._adapt(entity) for entity in entities), conn)

    async def exists(self, id_: GuildHistoryId, conn: None | Connection = None) -> bool:
        SQL = f"SELECT COUNT(*) AS count FROM `{self.table_name}` WHERE `name` = %(name)s AND `datetime` = %(datetime)s"
        result = await self._db.fetch(SQL, self._adapt_id(id_), conn)
        return result[0].get("count", 0) > 0

    async def count(self, conn: None | Connection = None) -> float:
        SQL = f"SELECT COUNT(*) AS count FROM `{self.table_name}`"
        return (await self._db.fetch(SQL, connection=conn))[0].get("count", 0)

    async def find_one(self, id_: GuildHistoryId, conn: None | Connection = None) -> None | GuildHistory:
        SQL = f"SELECT * FROM `{self.table_name}` WHERE `name` = %(name)s AND `datetime` = %(datetime)s"
        result = await self._db.fetch(SQL, self._adapt_id(id_), conn)
        return GuildHistory(**result[0]) if result else None

    async def find_all(self, conn: None | Connection = None) -> list[GuildHistory]:
        SQL = f"SELECT * FROM `{self.table_name}`"
        result = await self._db.fetch(SQL, connection=conn)
        return [GuildHistory(**row) for row in result] if result else []

    async def update(self, entities: Iterable[GuildHistory], conn: None | Connection = None) -> int:
        SQL = f"""
            UPDATE `{self.table_name}`
            SET `level` = %(level)s, `territories` = %(territories)s, `wars` = %(wars)s, `member_total` = %(member_total)s,
                `online_members` = %(online_members)s
            WHERE `name` = %(name)s AND `datetime` = %(datetime)s
        """
        return await self._db.execute_many(SQL, tuple(self._adapt(entity) for entity in entities), conn)

    async def delete(self, id_: GuildHistoryId, conn: None | Connection = None) -> int:
        SQL = f"DELETE FROM `{self.table_name}` WHERE `name` = %(name)s AND `datetime` = %(datetime)s"
        return await self._db.execute(SQL, self._adapt_id(id_), conn)

    async def create_table(self, conn: None | Connection = None) -> None:
        SQL = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                `name` varchar(30) NOT NULL,
                `level` decimal(5,2) unsigned NOT NULL,
                `territories` smallint unsigned NOT NULL,
                `wars` int unsigned NOT NULL,
                `member_total` tinyint unsigned NOT NULL,
                `online_members` tinyint unsigned NOT NULL,
                `datetime` datetime NOT NULL,
                UNIQUE KEY `guildHistory_uq_NameDt` (`name`,`datetime`),
                KEY `guildHistory_idx_NameDt` (`name`,`datetime`) /*!80000 INVISIBLE */
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(SQL)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
