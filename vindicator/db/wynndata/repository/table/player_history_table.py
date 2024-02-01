from __future__ import annotations
from typing import TYPE_CHECKING

from vindicator import PlayerHistoryBase

if TYPE_CHECKING:
    from vindicator import (
        DatabaseQuery,
        PlayerHistory,
        PlayerHistoryId
    )


class PlayerHistoryTable(PlayerHistoryBase):

    _TABLE_NAME: str = "player_history"

    def __init__(self, db: DatabaseQuery) -> None:
        self._db = db

    async def insert(self, entity: PlayerHistory) -> bool:
        sql = f"""
        INSERT INTO {self.table_name}
        (guild_name, guild_rank, playtime, support_rank, `rank`, datetime, username, uuid)
        VALUES
        (?, ?, ?, ?, ?, ?, ?, ?)
        ON DUPLICATE KEY UPDATE
        datetime = VALUES(datetime)
        """
        await self._db.execute_fetch(sql, (
            entity.guild_name,
            entity.guild_rank,
            entity.playtime,
            entity.support_rank,
            entity.rank,
            entity.datetime,
            entity.username,
            entity.uuid
        ))
        return True

    async def exists(self, id: PlayerHistoryId) -> bool: ...

    async def count(self) -> float: ...

    async def find_one(self, id: PlayerHistoryId) -> None | PlayerHistory: ...

    async def find_all(self) -> None | list[PlayerHistory]: ...

    async def update(self, entity: PlayerHistory) -> bool: ...

    async def delete(self, id: PlayerHistoryId) -> bool: ...

    async def create_table(self) -> None:
        sql = f"""
        CREATE TABLE IF NOT EXISTS `{self.table_name}` (
            `uuid` binary(16) NOT NULL,
            `username` varchar(16) NOT NULL,
            `support_rank` varchar(45) DEFAULT NULL,
            `playtime` decimal(7,2) unsigned NOT NULL,
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
