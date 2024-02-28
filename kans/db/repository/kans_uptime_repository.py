from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

from . import Repository
from ..model import KansUptime, KansUptimeId

if TYPE_CHECKING:
    from aiomysql import Connection


class KansUptimeRepository(Repository[KansUptime, KansUptimeId]):

    _TABLE_NAME = "kans_uptime"

    async def insert(self, entities: Iterable[KansUptime], conn: None | Connection = None) -> int:
        SQL = f"""
            REPLACE INTO `{self.table_name}` (`start_time`, `stop_time`)
            VALUES (%(start_time)s, %(stop_time)s)
        """
        return await self._db.execute_many(SQL, tuple(entity.to_dict() for entity in entities), conn)

    async def exists(self, id_: KansUptimeId, conn: None | Connection = None) -> bool: ...
    async def count(self, conn: None | Connection = None) -> float: ...
    async def find_one(self, id_: KansUptimeId, conn: None | Connection = None) -> None | KansUptime: ...
    async def find_all(self, conn: None | Connection = None) -> None | list[KansUptime]: ...
    async def update(self, entities: Iterable[KansUptime], conn: None | Connection = None) -> int: ...
    async def delete(self, id_: KansUptimeId, conn: None | Connection = None) -> int: ...
    async def create_table(self, conn: None | Connection = None) -> None:
        SQL = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                `nth` int NOT NULL AUTO_INCREMENT,
                `start_time` datetime NOT NULL,
                `stop_time` datetime NOT NULL,
                PRIMARY KEY (`nth`),
                UNIQUE KEY `start_time_UNIQUE` (`start_time`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(SQL)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
