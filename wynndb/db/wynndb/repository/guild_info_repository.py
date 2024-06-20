from __future__ import annotations
from typing import Iterable, TYPE_CHECKING

from . import Repository
from ..model import GuildInfo

if TYPE_CHECKING:
    from aiomysql import Connection


class GuildInfoRepository(Repository[GuildInfo]):

    _TABLE_NAME: str = "guild_info"

    async def insert(self, entities: Iterable[GuildInfo], conn: None | Connection = None) -> int:
        # NOTE: This doesn't change. Ignore duplicates.
        SQL = f"""
            INSERT IGNORE INTO `{self.table_name}` (`uuid`, `name`, `prefix`, `created`)
            VALUES (%(uuid)s, %(name)s, %(prefix)s, %(created)s)
        """
        return await self._db.execute_many(SQL, (self._adapt(entity) for entity in entities), conn)

    async def create_table(self, conn: None | Connection = None) -> None:
        SQL = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                `name` varchar(30) NOT NULL,
                `prefix` varchar(4) NOT NULL,
                `created` datetime NOT NULL,
                `uuid` binary(16) NOT NULL,
                PRIMARY KEY (`name`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(SQL)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
