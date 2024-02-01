from __future__ import annotations
from typing import TYPE_CHECKING

from vindicator import GuildHistoryBase

if TYPE_CHECKING:
    from vindicator import (
        DatabaseQuery,
        GuildHistory,
        GuildHistoryId
    )


class GuildHistoryTable(GuildHistoryBase):

    _TABLE_NAME: str = "guild_history"

    def __init__(self, db: DatabaseQuery) -> None:
        self._db = db

    async def insert(self, entity: GuildHistory) -> bool:
        sql = f"""
        INSERT IGNORE INTO {self.table_name} (level, member_total, name, online_members, territories, wars, datetime)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        await self._db.execute_fetch(sql, (
            entity.level,
            entity.member_total,
            entity.name
        ))
        return True

    async def exists(self, id_: GuildHistoryId) -> bool: ...

    async def count(self) -> float: ...

    async def find_one(self, id_: GuildHistoryId) -> None | GuildHistory: ...

    async def find_all(self) -> None | list[GuildHistory]: ...

    async def update(self, entity: GuildHistory) -> bool: ...

    async def delete(self, id_: GuildHistoryId) -> bool: ...

    async def create_table(self) -> None:
        sql = f"""
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
        await self._db.execute(sql)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
