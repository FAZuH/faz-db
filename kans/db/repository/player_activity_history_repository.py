from __future__ import annotations
from typing import TYPE_CHECKING, Any, Iterable

from kans import PlayerActivityHistory, Repository

if TYPE_CHECKING:
    from aiomysql import Connection
    from kans import DatabaseQuery


class PlayerActivityHistoryRepository(Repository[PlayerActivityHistory]):
    """implements `PlayerActivityHistoryRepo`"""

    _TABLE_NAME: str = "player_activity_history"

    def __init__(self, db: DatabaseQuery) -> None:
        self._db = db

    async def insert(self, entities: Iterable[PlayerActivityHistory], conn: None | Connection = None) -> int:
        sql = (
        f"REPLACE INTO `{self.table_name}` (`uuid`, `logon_datetime`, `logoff_datetime`) "
        "VALUES (%s, %s, %s)"
        )
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
            KEY `player_uptime_fk_uuid_idx` (`uuid`),
            KEY `player_uptime_idx_logon_timestamp` (`logon_datetime` DESC)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(sql)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
