from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

from . import Repository
from ..model import KansUptime, KansUptimeId

if TYPE_CHECKING:
    from aiomysql import Connection


class KansUptimeRepository(Repository[KansUptime, KansUptimeId]):

    _TABLE_NAME: str = "kans_uptime"

    async def insert(self, entities: Iterable[KansUptime], conn: None | Connection = None) -> int:
        SQL = f"""
            REPLACE INTO `{self.table_name}` (`start_time`, `stop_time`)
            VALUES (%(start_time)s, %(stop_time)s)
        """
        return await self._db.execute_many(SQL, tuple(self._adapt(entity) for entity in entities), conn)

    async def exists(self, id_: KansUptimeId, conn: None | Connection = None) -> bool:
        SQL = f"SELECT COUNT(*) FROM `{self.table_name}` WHERE `start_time` = %(start_time)s"
        return (await self._db.fetch(SQL, self._adapt_id(id_), connection=conn))[0].get("COUNT(*)", 0) > 0

    async def count(self, conn: None | Connection = None) -> float:
        SQL = f"SELECT COUNT(*) FROM `{self.table_name}`"
        return (await self._db.fetch(SQL, connection=conn))[0].get("COUNT(*)", 0)

    async def find_one(self, id_: KansUptimeId, conn: None | Connection = None) -> None | KansUptime:
        SQL = f"SELECT * FROM `{self.table_name}` WHERE `start_time` = %(start_time)s"
        result = await self._db.fetch(SQL, self._adapt_id(id_), conn)
        return KansUptime(**result[0]) if result else None

    async def find_all(self, conn: None | Connection = None) -> list[KansUptime]:
        SQL = f"SELECT * FROM `{self.table_name}`"
        result = await self._db.fetch(SQL, connection=conn)
        return [KansUptime(**row) for row in result] if result else []

    async def update(self, entities: Iterable[KansUptime], conn: None | Connection = None) -> int:
        SQL = f"""
            UPDATE `{self.table_name}`
            SET `stop_time` = %(stop_time)s
            WHERE `start_time` = %(start_time)s
        """
        return await self._db.execute_many(SQL, tuple(self._adapt(entity) for entity in entities), conn)

    async def delete(self, id_: KansUptimeId, conn: None | Connection = None) -> int:
        SQL = f"DELETE FROM `{self.table_name}` WHERE `start_time` = %(start_time)s"
        return await self._db.execute(SQL, self._adapt_id(id_), conn)

    async def create_table(self, conn: None | Connection = None) -> None:
        SQL = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                `start_time` datetime NOT NULL,
                `stop_time` datetime NOT NULL,
                PRIMARY KEY (`start_time`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(SQL, connection=conn)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
