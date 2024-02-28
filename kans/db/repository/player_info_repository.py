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
            VALUES (%s, %s, %s)
        """
        return await self._db.execute_many(SQL, tuple(entity.to_tuple() for entity in entities), conn)

    async def exists(self, id_: PlayerInfoId, conn: None | Connection = None) -> bool: ...

    async def count(self, conn: None | Connection = None) -> float:
        SQL = f"SELECT COUNT(*) FROM `{self.table_name}`"
        return (await self._db.fetch(SQL, connection=conn))[0].get("COUNT(*)", 0)

    async def find_one(self, id_: PlayerInfoId, conn: None | Connection = None) -> None | PlayerInfo: ...

    async def find_all(self, conn: None | Connection = None) -> None | list[PlayerInfo]: ...

    async def update(self, entities: Iterable[PlayerInfo], conn: None | Connection = None) -> int: ...

    async def delete(self, id_: PlayerInfoId, conn: None | Connection = None) -> int: ...

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
