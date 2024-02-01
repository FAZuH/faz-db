from __future__ import annotations
from typing import TYPE_CHECKING

from vindicator import PlayerInfoBase

if TYPE_CHECKING:
    from vindicator import (
        DatabaseQuery,
        PlayerInfo,
        PlayerInfoId
    )


class PlayerInfoTable(PlayerInfoBase):

    _TABLE_NAME: str = "player_info"

    def __init__(self, db: DatabaseQuery) -> None:
        self._db = db

    async def insert(self, entity: PlayerInfo) -> bool:
        sql = f"""
        REPLACE INTO {self.table_name} (first_join, latest_username, uuid)
        VALUES (?, ?, ?)
        """
        # ON DUPLICATE KEY UPDATE
        # latest_username = CASE
        #     WHEN VALUES(latest_username) <> latest_username THEN VALUES(latest_username)
        #     ELSE latest_username
        # END
        await self._db.execute_fetch(sql, (
            entity.first_join,
            entity.latest_username,
            entity.uuid
        ))
        return True

    async def exists(self, id_: PlayerInfoId) -> bool: ...

    async def count(self) -> float: ...

    async def find_one(self, id_: PlayerInfoId) -> None | PlayerInfo: ...

    async def find_all(self) -> None | list[PlayerInfo]: ...

    async def update(self, entity: PlayerInfo) -> bool: ...

    async def delete(self, id_: PlayerInfoId) -> bool: ...

    async def create_table(self) -> None:
        sql = f"""
        CREATE TABLE IF NOT EXISTS `{self.table_name}` (
            `uuid` binary(16) NOT NULL,
            `latest_username` varchar(16) NOT NULL,
            `first_join` datetime NOT NULL,
            PRIMARY KEY (`uuid`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(sql)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
