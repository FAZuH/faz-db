from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

from . import Repository
from ..model import PlayerInfo, PlayerInfoId

if TYPE_CHECKING:
    from aiomysql import Connection


class PlayerInfoRepository(Repository[PlayerInfo, PlayerInfoId]):

    _TABLE_NAME: str = "player_info"

    async def insert(self, entities: Iterable[PlayerInfo], conn: None | Connection = None) -> int:
        SQL = f"""
            REPLACE INTO `{self.table_name}` (`uuid`, `latest_username`, `first_join`)
            VALUES (%(uuid)s, %(latest_username)s, %(first_join)s)
        """
        return await self._db.execute_many(SQL, tuple(self._adapt(entity) for entity in entities), conn)

    async def exists(self, id_: PlayerInfoId, conn: None | Connection = None) -> bool:
        SQL = f"SELECT COUNT(*) AS count FROM `{self.table_name}` WHERE `uuid` = %(uuid)s"
        result = await self._db.fetch(SQL, self._adapt_id(id_), connection=conn)
        return result[0].get("count", 0) > 0

    async def count(self, conn: None | Connection = None) -> float:
        SQL = f"SELECT COUNT(*) FROM `{self.table_name}`"
        return (await self._db.fetch(SQL, connection=conn))[0].get("COUNT(*)", 0)

    async def find_one(self, id_: PlayerInfoId, conn: None | Connection = None) -> None | PlayerInfo:
        SQL = f"SELECT * FROM `{self.table_name}` WHERE `uuid` = %(uuid)s"
        result = await self._db.fetch(SQL, self._adapt_id(id_), connection=conn)
        return PlayerInfo(**result[0]) if result else None

    async def find_all(self, conn: None | Connection = None) -> list[PlayerInfo]:
        SQL = f"SELECT * FROM `{self.table_name}`"
        result = await self._db.fetch(SQL, connection=conn)
        return [PlayerInfo(**row) for row in result] if result else []

    async def update(self, entities: Iterable[PlayerInfo], conn: None | Connection = None) -> int:
        SQL = f"""
            UPDATE `{self.table_name}`
            SET `latest_username` = %(latest_username)s, `first_join` = %(first_join)s
            WHERE `uuid` = %(uuid)s
        """
        return await self._db.execute_many(SQL, tuple(self._adapt(entity) for entity in entities), conn)

    async def delete(self, id_: PlayerInfoId, conn: None | Connection = None) -> int:
        SQL = f"DELETE FROM `{self.table_name}` WHERE `uuid` = %(uuid)s"
        return await self._db.execute(SQL, self._adapt_id(id_), conn)

    async def create_table(self, conn: None | Connection = None) -> None:
        SQL = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                `uuid` binary(16) NOT NULL,
                `latest_username` varchar(16) NOT NULL,
                `first_join` datetime NOT NULL,
                PRIMARY KEY (`uuid`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(SQL)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
