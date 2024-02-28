from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

from . import Repository
from ..model import PlayerActivityHistory, PlayerActivityHistoryId

if TYPE_CHECKING:
    from aiomysql import Connection


class PlayerActivityHistoryRepository(Repository[PlayerActivityHistory, PlayerActivityHistoryId]):

    _TABLE_NAME: str = "player_activity_history"

    async def insert(self, entities: Iterable[PlayerActivityHistory], conn: None | Connection = None) -> int:
        SQL = f"""
            REPLACE INTO `{self.table_name}` (`uuid`, `logon_datetime`, `logoff_datetime`)
            VALUES (%(uuid)s, %(logon_datetime)s, %(logoff_datetime)s)
        """
        return await self._db.execute_many(SQL, tuple(entity.to_dict() for entity in entities), conn)

    async def exists(self, id_: PlayerActivityHistoryId, conn: None | Connection = None) -> bool:
        SQL = f"SELECT COUNT(*) AS count FROM `{self.table_name}` WHERE `uuid` = %(uuid)s"
        result = await self._db.fetch(SQL, {"uuid": id_.uuid}, connection=conn)
        return result[0].get("count", 0) > 0

    async def count(self, conn: None | Connection = None) -> float:
        SQL = f"SELECT COUNT(*) FROM `{self.table_name}`"
        return (await self._db.fetch(SQL, connection=conn))[0].get("COUNT(*)", 0)

    async def find_one(self, id_: PlayerActivityHistoryId, conn: None | Connection = None) -> None | PlayerActivityHistory:
        SQL = f"SELECT * FROM `{self.table_name}` WHERE `uuid` = %(uuid)s"
        result = await self._db.fetch(SQL, {"uuid": id_.uuid}, connection=conn)
        return PlayerActivityHistory(**result[0]) if result else None

    async def find_all(self, conn: None | Connection = None) -> None | list[PlayerActivityHistory]:
        SQL = f"SELECT * FROM `{self.table_name}`"
        result = await self._db.fetch(SQL, connection=conn)
        return [PlayerActivityHistory(**row) for row in result] if result else None

    async def update(self, entities: Iterable[PlayerActivityHistory], conn: None | Connection = None) -> int:
        SQL = f"""
            UPDATE `{self.table_name}`
            SET `logon_datetime` = %(logon_datetime)s, `logoff_datetime` = %(logoff_datetime)s
            WHERE `uuid` = %(uuid)s
        """
        return await self._db.execute_many(SQL, tuple(entity.to_dict() for entity in entities), conn)

    async def delete(self, id_: PlayerActivityHistoryId, conn: None | Connection = None) -> int:
        SQL = f"DELETE FROM `{self.table_name}` WHERE `uuid` = %(uuid)s"
        return await self._db.execute(SQL, {"uuid": id_.uuid}, conn)

    async def create_table(self, conn: None | Connection = None) -> None:
        SQL = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                `uuid` binary(16) NOT NULL,
                `logon_datetime` datetime NOT NULL,
                `logoff_datetime` datetime NOT NULL,
                UNIQUE KEY `player_uptime_uq_uuidlogon` (`uuid`,`logon_datetime`),
                KEY `player_uptime_idx_logon_timestamp` (`logon_datetime` DESC)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(SQL)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
