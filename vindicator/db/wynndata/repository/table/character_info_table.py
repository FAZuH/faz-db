from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

from vindicator import CharacterInfoRepo

if TYPE_CHECKING:
    from aiomysql import Connection
    from vindicator import (
        CharacterInfo,
        CharacterInfoId,
        DatabaseQuery
    )


class CharacterInfoTable(CharacterInfoRepo):

    _TABLE_NAME: str = "character_info"

    def __init__(self, db: DatabaseQuery) -> None:
        self._db = db

    async def insert(self, connection: None | Connection, entity: Iterable[CharacterInfo]) -> bool:
        # NOTE: This doesn't change. Ignore duplicates.
        sql = f"""
        INSERT IGNORE INTO {self.table_name} (character_uuid, type, uuid)
        VALUES (%s, %s, %s)
        """
        await self._db.fetch(sql, (
            entity.character_uuid,
            entity.type,
            entity.uuid
        ))
        return True

    async def exists(self, id_: CharacterInfoId) -> bool: ...

    async def count(self) -> float: ...

    async def find_one(self, id_: CharacterInfoId) -> None | CharacterInfo: ...

    async def find_all(self) -> None | list[CharacterInfo]: ...

    async def update(self, entity: CharacterInfo) -> bool: ...

    async def delete(self, id_: CharacterInfoId) -> bool: ...

    async def create_table(self) -> None:
        sql = f"""
        CREATE TABLE IF NOT EXISTS `{self.table_name}` (
            `character_uuid` binary(16) NOT NULL,
            `uuid` binary(16) NOT NULL,
            `type` enum('ARCHER','ASSASSIN','MAGE','SHAMAN','WARRIOR') NOT NULL,
            PRIMARY KEY (`character_uuid`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(sql)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
