from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

from aiomysql import Connection

from . import Repository
from ..model import CharacterHistory, CharacterHistoryId

if TYPE_CHECKING:
    from aiomysql import Connection


class CharacterHistoryRepository(Repository[CharacterHistory, CharacterHistoryId]):

    _TABLE_NAME: str = "character_history"

    async def insert(self, entities: Iterable[CharacterHistory], conn: None | Connection = None) -> int:
        SQL = f"""
            INSERT IGNORE INTO `{self.table_name}` (
                `character_uuid`, `level`, `xp`, `wars`, `playtime`, `mobs_killed`, `chests_found`, `logins`,
                `deaths`, `discoveries`, `gamemode`, `alchemism`, `armouring`, `cooking`, `jeweling`, `scribing`,
                `tailoring`, `weaponsmithing`, `woodworking`, `mining`, `woodcutting`, `farming`, `fishing`,
                `dungeon_completions`, `quest_completions`, `raid_completions`, `datetime`
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        return await self._db.execute_many(SQL, tuple(entity.to_tuple() for entity in entities), conn)

    async def exists(self, id_: CharacterHistoryId, conn: None | Connection = None) -> bool:
        SQL = f"SELECT COUNT(*) AS count FROM `{self.table_name}` WHERE `character_uuid` = %s AND `datetime` = %s"
        result = await self._db.fetch(SQL, (id_.character_uuid, id_.datetime), connection=conn)
        return result[0].get("count", 0) > 0

    async def count(self, conn: None | Connection = None) -> float:
        SQL = f"SELECT COUNT(*) AS count FROM `{self.table_name}`"
        result =await self._db.fetch(SQL, connection=conn)
        return result[0].get("count", 0)

    async def find_one(self, id_: CharacterHistoryId, conn: None | Connection = None) -> None | CharacterHistory:
        SQL = f"SELECT * FROM `{self.table_name}` WHERE `character_uuid` = %s AND `datetime` = %s"
        result = await self._db.fetch(SQL, (id_.character_uuid, id_.datetime), connection=conn)
        return CharacterHistory(**result[0]) if result else None

    async def find_all(self, conn: None | Connection = None) -> None | list[CharacterHistory]:
        SQL = f"SELECT * FROM `{self.table_name}`"
        result = await self._db.fetch(SQL, connection=conn)
        return [CharacterHistory(**row) for row in result] if result else None

    async def update(self, entities: Iterable[CharacterHistory], conn: None | Connection = None) -> int:
        SQL = f"""
            UPDATE `{self.table_name}`
            SET `alchemism` = %s, `armouring` = %s, `cooking` = %s, `farming` = %s, `fishing` = %s, `jeweling` = %s,
                `mining` = %s, `scribing` = %s, `tailoring` = %s, `weaponsmithing` = %s, `woodcutting` = %s,
                `woodworking` = %s, `chests_found` = %s, `deaths` = %s, `discoveries` = %s, `level` = %s, `logins` = %s,
                `mobs_killed` = %s, `playtime` = %s, `wars` = %s, `xp` = %s, `dungeon_completions` = %s,
                `quest_completions` = %s, `raid_completions` = %s, `gamemode` = %s
            WHERE `character_uuid` = %s AND `datetime` = %s
        """
        return await self._db.execute_many(
                SQL,
                tuple(entity.to_tuple() for entity in entities),
                conn
        )

    async def delete(self, id_: CharacterHistoryId, conn: None | Connection = None) -> int: ...

    async def create_table(self, conn: None | Connection = None) -> None:
        SQL = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                `character_uuid` binary(16) NOT NULL,
                `level` tinyint unsigned NOT NULL,
                `xp` bigint unsigned NOT NULL,
                `wars` int unsigned NOT NULL,
                `playtime` decimal(7,2) unsigned NOT NULL,
                `mobs_killed` int unsigned NOT NULL,
                `chests_found` int unsigned NOT NULL,
                `logins` int unsigned NOT NULL,
                `deaths` int unsigned NOT NULL,
                `discoveries` int unsigned NOT NULL,
                `gamemode` bit(5) NOT NULL,
                `alchemism` decimal(5,2) unsigned NOT NULL,
                `armouring` decimal(5,2) unsigned NOT NULL,
                `cooking` decimal(5,2) unsigned NOT NULL,
                `jeweling` decimal(5,2) unsigned NOT NULL,
                `scribing` decimal(5,2) unsigned NOT NULL,
                `tailoring` decimal(5,2) unsigned NOT NULL,
                `weaponsmithing` decimal(5,2) unsigned NOT NULL,
                `woodworking` decimal(5,2) unsigned NOT NULL,
                `mining` decimal(5,2) unsigned NOT NULL,
                `woodcutting` decimal(5,2) unsigned NOT NULL,
                `farming` decimal(5,2) unsigned NOT NULL,
                `fishing` decimal(5,2) unsigned NOT NULL,
                `dungeon_completions` int unsigned NOT NULL,
                `quest_completions` int unsigned NOT NULL,
                `raid_completions` int unsigned NOT NULL,
                `datetime` datetime NOT NULL,
                KEY `player_character_idx_ts` (`datetime` DESC)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(SQL, connection=conn)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
