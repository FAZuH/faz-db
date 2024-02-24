from __future__ import annotations
from typing import TYPE_CHECKING, Any, Iterable

from kans import PlayerHistory, Repository

if TYPE_CHECKING:
    from aiomysql import Connection
    from kans import DatabaseQuery


class PlayerHistoryRepository(Repository[PlayerHistory]):

    _TABLE_NAME: str = "player_history"

    def __init__(self, db: DatabaseQuery) -> None:
        self._db = db

    async def insert(self, entities: Iterable[PlayerHistory], conn: None | Connection = None) -> int:
        sql = (
        f"INSERT INTO `{self.table_name}` "
        "(`guild_name`, `guild_rank`, `playtime`, `support_rank`, `rank`, `datetime`, `username`, `uuid`) "
        "VALUES "
        "(%s, %s, %s, %s, %s, %s, %s, %s) "
        "ON DUPLICATE KEY UPDATE "
        "`datetime` = VALUES(`datetime`)"
        )
        return await self._db.execute_many(
            sql,
            tuple((
                entity.guild_name,
                entity.guild_rank,
                entity.playtime,
                entity.support_rank,
                entity.rank,
                entity.datetime.datetime,
                entity.username,
                entity.uuid.uuid
            ) for entity in entities),
            conn
        )

    async def exists(self,id_: Any, conn: None | Connection = None) -> bool: ...

    async def count(self, conn: None | Connection = None) -> float:
        sql = f"SELECT COUNT(*) FROM `{self.table_name}`"
        return (await self._db.fetch(sql, connection=conn))[0].get("COUNT(*)", 0)

    async def find_one(self, id_: Any, conn: None | Connection = None) -> None | PlayerHistory: ...

    async def find_all(self, conn: None | Connection = None) -> None | list[PlayerHistory]: ...

    async def update(self, entities: Iterable[PlayerHistory], conn: None | Connection = None) -> int: ...

    async def delete(self, id_: Any, conn: None | Connection = None) -> int: ...

    async def create_table(self, conn: None | Connection = None) -> None:
        sql = f"""
        CREATE TABLE IF NOT EXISTS `{self.table_name}` (
            `uuid` binary(16) NOT NULL,
            `username` varchar(16) NOT NULL,
            `support_rank` varchar(45) DEFAULT NULL,
            `playtime` decimal(8,2) unsigned NOT NULL,
            `guild_name` varchar(30) DEFAULT NULL,
            `guild_rank` enum('OWNER','CHIEF','STRATEGIST','CAPTAIN','RECRUITER','RECRUIT') DEFAULT NULL,
            `rank` varchar(30) DEFAULT NULL,
            `datetime` datetime NOT NULL,
            KEY `player_main_idx_ts` (`datetime` DESC)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(sql)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
