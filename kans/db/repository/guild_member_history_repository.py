from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

from . import Repository
from ..model import GuildMemberHistory, GuildMemberHistoryId

if TYPE_CHECKING:
    from aiomysql import Connection
    from kans.db import DatabaseQuery
    from kans.util import DbModelDictAdapter, DbModelIdDictAdapter



class GuildMemberHistoryRepository(Repository[GuildMemberHistory, GuildMemberHistoryId]):

    _TABLE_NAME: str = "guild_member_history"

    def __init__(
        self,
        db: DatabaseQuery,
        db_model_dict_adapter: DbModelDictAdapter,
        db_model_id_dict_adapter: DbModelIdDictAdapter
    ) -> None:
        super().__init__(db)
        self._adapt = db_model_dict_adapter.from_guild_member_history
        self._adapt_id = db_model_id_dict_adapter.from_guild_member_history

    async def insert(self, entities: Iterable[GuildMemberHistory], conn: None | Connection = None) -> int:
        SQL = f"""
            INSERT IGNORE INTO `{self.table_name}` (`uuid`, `contributed`, `joined`, `datetime`)
            VALUES (%(uuid)s, %(contributed)s, %(joined)s, %(datetime)s)
        """
        return await self._db.execute_many(SQL, tuple(self._adapt(entity) for entity in entities), conn)

    async def exists(self, id_: GuildMemberHistoryId, conn: None | Connection = None) -> bool:
        SQL = f"SELECT COUNT(*) AS count FROM `{self.table_name}` WHERE `uuid` = %(uuid)s"
        result = await self._db.fetch(SQL, self._adapt_id(id_), connection=conn)
        return result[0].get("count", 0) > 0

    async def count(self, conn: None | Connection = None) -> float:
        SQL = f"SELECT COUNT(*) FROM `{self.table_name}`"
        return (await self._db.fetch(SQL, connection=conn))[0].get("COUNT(*)", 0)

    async def find_one(self, id_: GuildMemberHistoryId, conn: None | Connection = None) -> None | GuildMemberHistory:
        SQL = f"SELECT * FROM `{self.table_name}` WHERE `uuid` = %(uuid)s"
        result = await self._db.fetch(SQL, self._adapt_id(id_), connection=conn)
        return GuildMemberHistory(**result[0]) if result else None

    async def find_all(self, conn: None | Connection = None) -> None | list[GuildMemberHistory]:
        SQL = f"SELECT * FROM `{self.table_name}`"
        result = await self._db.fetch(SQL, connection=conn)
        return [GuildMemberHistory(**row) for row in result] if result else None

    async def update(self, entities: Iterable[GuildMemberHistory], conn: None | Connection = None) -> int:
        SQL = f"""
            UPDATE `{self.table_name}`
            SET `contributed` = %(contributed)s, `joined` = %(joined)s, `datetime` = %(datetime)s
            WHERE `uuid` = %(uuid)s
        """
        return await self._db.execute_many(SQL, tuple(self._adapt(entity) for entity in entities), conn)

    async def delete(self, id_: GuildMemberHistoryId, conn: None | Connection = None) -> int:
        SQL = f"DELETE FROM `{self.table_name}` WHERE `uuid` = %(uuid)s"
        return await self._db.execute(SQL, self._adapt_id(id_), conn)

    async def create_table(self, conn: None | Connection = None) -> None:
        SQL = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                `uuid` binary(16) NOT NULL,
                `contributed` bigint unsigned NOT NULL,
                `joined` datetime NOT NULL,
                `datetime` datetime NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(SQL)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
