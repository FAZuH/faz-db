from __future__ import annotations
from typing import TYPE_CHECKING

from vindicator import GuildInfoBase

if TYPE_CHECKING:
    from vindicator import (
        DatabaseQuery,
        GuildInfo,
        GuildInfoId
    )


class GuildInfoTable(GuildInfoBase):

    _TABLE_NAME: str = "guild_info"

    def __init__(self, db: DatabaseQuery) -> None:
        self._db = db

    async def insert(self, entity: GuildInfo) -> bool:
        # NOTE: This doesn't change. Ignore duplicates.
        sql = f"""
        INSERT IGNORE INTO {self.table_name} (created, name, prefix)
        VALUES (?, ?, ?)
        """
        await self._db.execute_fetch(sql, (
            entity.created,
            entity.name,
            entity.prefix
        ))
        return True

    async def exists(self, id_: GuildInfoId) -> bool: ...

    async def count(self) -> float: ...

    async def find_one(self, id_: GuildInfoId) -> None | GuildInfo: ...

    async def find_all(self) -> None | list[GuildInfo]: ...

    async def update(self, entity: GuildInfo) -> bool: ...

    async def delete(self, id_: GuildInfoId) -> bool: ...

    async def create_table(self) -> None:
        sql = f"""
        CREATE TABLE IF NOT EXISTS `{self.table_name}` (
            `name` varchar(30) NOT NULL,
            `prefix` varchar(4) NOT NULL,
            `created` datetime NOT NULL,
            PRIMARY KEY (`name`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(sql)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
