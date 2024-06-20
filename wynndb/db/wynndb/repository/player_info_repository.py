from __future__ import annotations
from typing import Iterable, TYPE_CHECKING

from . import Repository
from ..model import PlayerInfo

if TYPE_CHECKING:
    from aiomysql import Connection


class PlayerInfoRepository(Repository[PlayerInfo]):

    _TABLE_NAME: str = "player_info"

    async def insert(self, entities: Iterable[PlayerInfo], conn: None | Connection = None) -> int:
        SQL = f"""
            REPLACE INTO `{self.table_name}` (`uuid`, `latest_username`, `first_join`)
            VALUES (%(uuid)s, %(latest_username)s, %(first_join)s)
        """
        return await self._db.execute_many(SQL, tuple(self._adapt(entity) for entity in entities), conn)

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
