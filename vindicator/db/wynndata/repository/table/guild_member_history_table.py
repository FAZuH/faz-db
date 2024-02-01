from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

from vindicator import GuildMemberHistoryRepo

if TYPE_CHECKING:
    from aiomysql import Connection
    from vindicator import (
        DatabaseQuery,
        GuildMemberHistory,
        GuildMemberHistoryId
    )


class GuildMemberHistoryTable(GuildMemberHistoryRepo):

    _TABLE_NAME: str = "guild_member_history"

    def __init__(self, db: DatabaseQuery) -> None:
        self._db = db

    async def insert(self, entities: Iterable[GuildMemberHistory], conn: None | Connection = None) -> int:
        sql = f"""
        INSERT IGNORE INTO {self.table_name} (joined, uuid, contributed, datetime)
        VALUES (%s, %s, %s, %s)
        """
        await self._db.execute_many(
            sql,
            tuple((
                entity.joined,
                entity.uuid,
                entity.contributed,
                entity.datetime
            ) for entity in entities),
            conn
        )
        return True

    async def exists(self,id_: GuildMemberHistoryId, conn: None | Connection = None) -> bool: ...

    async def count(self, conn: None | Connection = None) -> float: ...

    async def find_one(self, id_: GuildMemberHistoryId, conn: None | Connection = None) -> None | GuildMemberHistory: ...

    async def find_all(self, conn: None | Connection = None) -> None | list[GuildMemberHistory]: ...

    async def update(self, entities: Iterable[GuildMemberHistory], conn: None | Connection = None) -> int: ...

    async def delete(self, id_: GuildMemberHistoryId, conn: None | Connection = None) -> int: ...

    async def create_table(self, conn: None | Connection = None) -> None:
        sql = f"""
        CREATE TABLE IF NOT EXISTS `{self.table_name}` (
            `uuid` binary(16) NOT NULL,
            `contributed` bigint unsigned NOT NULL,
            `joined` datetime NOT NULL,
            `datetime` datetime NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(sql)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
