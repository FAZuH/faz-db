from __future__ import annotations
from typing import TYPE_CHECKING, Any, Iterable

from . import Repository
from ..model import PlayerActivityHistory, PlayerActivityHistoryId

if TYPE_CHECKING:
    from decimal import Decimal
    from aiomysql import Connection
    from .. import DatabaseQuery


class PlayerActivityHistoryRepository(Repository[PlayerActivityHistory, PlayerActivityHistoryId]):

    _TABLE_NAME: str = "player_activity_history"

    def __init__(self, db: DatabaseQuery) -> None:
        self._db = db

    async def insert(self, entities: Iterable[PlayerActivityHistory], conn: None | Connection = None) -> int:
        sql = f"""
            REPLACE INTO `{self.table_name}` (`uuid`, `logon_datetime`, `logoff_datetime`)
            VALUES (%s, %s, %s)
        """
        return await self._db.execute_many(
                sql,
                tuple((
                        entity.uuid.uuid,
                        entity.logon_datetime.datetime,
                        entity.logoff_datetime.datetime
                ) for entity in entities),
                conn
        )

    async def exists(self, id_: Any, conn: None | Connection = None) -> bool: ...

    async def count(self, conn: None | Connection = None) -> float:
        sql = f"SELECT COUNT(*) FROM `{self.table_name}`"
        return (await self._db.fetch(sql, connection=conn))[0].get("COUNT(*)", 0)

    async def find_one(self, id_: Any, conn: None | Connection = None) -> None | PlayerActivityHistory: ...

    async def find_all(self, conn: None | Connection = None) -> None | list[PlayerActivityHistory]: ...

    async def update(self, entities: Iterable[PlayerActivityHistory], conn: None | Connection = None) -> int: ...

    async def delete(self, id_: Any, conn: None | Connection = None) -> int: ...

    async def create_table(self, conn: None | Connection = None) -> None:
        sql = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                `uuid` binary(16) NOT NULL,
                `logon_datetime` datetime NOT NULL,
                `logoff_datetime` datetime NOT NULL,
                UNIQUE KEY `player_uptime_uq_uuidlogon` (`uuid`,`logon_datetime`),
                KEY `player_uptime_idx_logon_timestamp` (`logon_datetime` DESC)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(sql)

    async def table_size(self, conn: Connection | None = None) -> Decimal:
        sql = f"""
            SELECT
                ROUND(((data_length + index_length)), 2) AS "size_bytes"
            FROM
                information_schema.TABLES
            WHERE
                table_schema = '{self._db.database}'
                AND table_name = '{self.table_name}';
        """
        res = await self._db.fetch(sql, connection=conn)
        return res[0].get("size_bytes", 0)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
