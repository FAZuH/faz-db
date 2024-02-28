from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

from . import Repository
from ..model import PlayerHistory, PlayerHistoryId

if TYPE_CHECKING:
    from aiomysql import Connection


class PlayerHistoryRepository(Repository[PlayerHistory, PlayerHistoryId]):

    _TABLE_NAME: str = "player_history"

    async def insert(self, entities: Iterable[PlayerHistory], conn: None | Connection = None) -> int:
        SQL = f"""
            INSERT INTO `{self.table_name}`
            (`uuid`, `username`, `support_rank`, `playtime`, `guild_name`, `guild_rank`, `rank`, `datetime`)
            VALUES
            (%(uuid)s, %(username)s, %(support_rank)s, %(playtime)s, %(guild_name)s, %(guild_rank)s, %(rank)s, %(datetime)s)
            ON DUPLICATE KEY UPDATE
            `datetime` = VALUES(`datetime`)
        """
        return await self._db.execute_many(SQL, tuple(entity.to_dict() for entity in entities), conn)

    async def exists(self,id_: PlayerHistoryId, conn: None | Connection = None) -> bool:
        SQL = f"SELECT COUNT(*) AS count FROM `{self.table_name}` WHERE `uuid` = %(uuid)s"
        result = await self._db.fetch(SQL, {"uuid": id_.uuid.uuid}, connection=conn)
        return result[0].get("count", 0) > 0

    async def count(self, conn: None | Connection = None) -> float:
        SQL = f"SELECT COUNT(*) FROM `{self.table_name}`"
        return (await self._db.fetch(SQL, connection=conn))[0].get("COUNT(*)", 0)

    async def find_one(self, id_: PlayerHistoryId, conn: None | Connection = None) -> None | PlayerHistory:
        SQL = f"SELECT * FROM `{self.table_name}` WHERE `uuid` = %(uuid)s"
        result = await self._db.fetch(SQL, {"uuid": id_.uuid.uuid}, connection=conn)
        return PlayerHistory(**result[0]) if result else None

    async def find_all(self, conn: None | Connection = None) -> None | list[PlayerHistory]:
        SQL = f"SELECT * FROM `{self.table_name}`"
        result = await self._db.fetch(SQL, connection=conn)
        return [PlayerHistory(**row) for row in result] if result else None

    async def update(self, entities: Iterable[PlayerHistory], conn: None | Connection = None) -> int:
        SQL = f"""
            UPDATE `{self.table_name}`
            SET `username` = %(username)s, `support_rank` = %(support_rank)s, `playtime` = %(playtime)s,
                `guild_name` = %(guild_name)s, `guild_rank` = %(guild_rank)s, `rank` = %(rank)s, `datetime` = %(datetime)s
            WHERE `uuid` = %(uuid)s
        """
        return await self._db.execute_many(SQL, tuple(entity.to_dict() for entity in entities), conn)

    async def delete(self, id_: PlayerHistoryId, conn: None | Connection = None) -> int:
        SQL = f"DELETE FROM `{self.table_name}` WHERE `uuid` = %(uuid)s"
        return await self._db.execute(SQL, {"uuid": id_.uuid.uuid}, conn)

    async def create_table(self, conn: None | Connection = None) -> None:
        SQL = f"""
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
        await self._db.execute(SQL)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
