from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

from . import Repository
from ..model import GuildHistory, GuildHistoryId

if TYPE_CHECKING:
    from aiomysql import Connection


class GuildHistoryRepository(Repository[GuildHistory, GuildHistoryId]):

    _TABLE_NAME: str = "guild_history"

    async def insert(self, entities: Iterable[GuildHistory], conn: None | Connection = None) -> int:
        SQL = f"""
            INSERT IGNORE INTO `{self.table_name}`
                (`name`, `level`, `territories`, `wars`, `member_total`, `online_members`, `datetime`)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        return await self._db.execute_many(SQL, tuple(entity.to_tuple() for entity in entities), conn)

    async def exists(self, id_: GuildHistoryId, conn: None | Connection = None) -> bool: ...

    async def count(self, conn: None | Connection = None) -> float:
        SQL = f"SELECT COUNT(*) FROM `{self.table_name}`"
        return (await self._db.fetch(SQL, connection=conn))[0].get("COUNT(*)", 0)

    async def find_one(self, id_: GuildHistoryId, conn: None | Connection = None) -> None | GuildHistory: ...

    async def find_all(self, conn: None | Connection = None) -> None | list[GuildHistory]: ...

    async def update(self, entities: Iterable[GuildHistory], conn: None | Connection = None) -> int: ...

    async def delete(self, id_: GuildHistoryId, conn: None | Connection = None) -> int: ...

    async def create_table(self, conn: None | Connection = None) -> None:
        SQL = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                `name` varchar(30) NOT NULL,
                `level` decimal(5,2) unsigned NOT NULL,
                `territories` smallint unsigned NOT NULL,
                `wars` int unsigned NOT NULL,
                `member_total` tinyint unsigned NOT NULL,
                `online_members` tinyint unsigned NOT NULL,
                `datetime` datetime NOT NULL,
                KEY `guildmain_fk_guildmaininfo_idx` (`name`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(SQL)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
