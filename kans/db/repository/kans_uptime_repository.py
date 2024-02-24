from __future__ import annotations
from typing import TYPE_CHECKING, Any, Iterable

from kans import KansUptime, Repository

if TYPE_CHECKING:
    from aiomysql import Connection
    from kans import DatabaseQuery


class KansUptimeRepository(Repository[KansUptime]):

    _TABLE_NAME = "kans_uptime"

    def __init__(self, db: DatabaseQuery) -> None:
        self._db = db

    async def insert(self, entities: Iterable[KansUptime], conn: None | Connection = None) -> int:
        sql = f"""
            REPLACE INTO `{self.table_name}` (`start_time`, `stop_time`)
            VALUES (%s, %s)
        """
        return await self._db.execute_many(
                sql,
                tuple((e.start_time, e.stop_time) for e in entities),
                conn
        )

    async def exists(self, id_: Any, conn: None | Connection = None) -> bool: ...
    async def count(self, conn: None | Connection = None) -> float: ...
    async def find_one(self, id_: Any, conn: None | Connection = None) -> None | KansUptime: ...
    async def find_all(self, conn: None | Connection = None) -> None | list[KansUptime]: ...
    async def update(self, entities: Iterable[KansUptime], conn: None | Connection = None) -> int: ...
    async def delete(self, id_: Any, conn: None | Connection = None) -> int: ...
    async def create_table(self, conn: None | Connection = None) -> None:
        sql = f"""
            CREATE TABLE `{self.table_name}` (
                `nth` int NOT NULL AUTO_INCREMENT,
                `start_time` datetime NOT NULL,
                `stop_time` datetime NOT NULL,
                PRIMARY KEY (`nth`),
                UNIQUE KEY `start_time_UNIQUE` (`start_time`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(sql)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
