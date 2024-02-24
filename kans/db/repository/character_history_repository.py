from __future__ import annotations
from typing import TYPE_CHECKING, Any, Iterable

from kans import CharacterHistory, Repository

if TYPE_CHECKING:
    from aiomysql import Connection
    from kans import DatabaseQuery


class CharacterHistoryRepository(Repository[CharacterHistory]):

    _TABLE_NAME: str = "character_history"

    def __init__(self, db: DatabaseQuery) -> None:
        self._db = db

    async def insert(self, entities: Iterable[CharacterHistory], conn: None | Connection = None) -> int:
        sql = (
        f"INSERT IGNORE INTO `{self.table_name}` ("
        "    `character_uuid`, `alchemism`, `armouring`, `cooking`, `farming`, `fishing`, `jeweling`, `mining`,"
        "    `scribing`, `tailoring`, `weaponsmithing`, `woodcutting`, `woodworking`, `chests_found`, `deaths`,"
        "    `discoveries`, `level`, `logins`, `mobs_killed`, `playtime`, `wars`, `xp`, `dungeon_completions`,"
        "    `quest_completions`, `raid_completions`, `gamemode`, `datetime`"
        ") "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        return await self._db.execute_many(
            sql,
            tuple((
                entity.character_uuid.uuid,
                entity.alchemism,
                entity.armouring,
                entity.cooking,
                entity.farming,
                entity.fishing,
                entity.jeweling,
                entity.mining,
                entity.scribing,
                entity.tailoring,
                entity.weaponsmithing,
                entity.woodcutting,
                entity.woodworking,
                entity.chests_found,
                entity.deaths,
                entity.discoveries,
                entity.level,
                entity.logins,
                entity.mobs_killed,
                entity.playtime,
                entity.wars,
                entity.xp,
                entity.dungeon_completions,
                entity.quest_completions,
                entity.raid_completions,
                entity.gamemode.gamemode,
                entity.datetime.datetime,
            ) for entity in entities),
            conn
        )

    async def exists(self, id_: Any, conn: None | Connection = None) -> bool: ...

    async def count(self, conn: None | Connection = None) -> float:
        sql = f"SELECT COUNT(*) FROM `{self.table_name}`"
        return (await self._db.fetch(sql, connection=conn))[0].get("COUNT(*)", 0)

    async def find_one(self, id_: Any, conn: None | Connection = None) -> None | CharacterHistory: ...

    async def find_all(self, conn: None | Connection = None) -> None | list[CharacterHistory]: ...

    async def update(self, entities: Iterable[CharacterHistory], conn: None | Connection = None) -> int: ...

    async def delete(self, id_: Any, conn: None | Connection = None) -> int: ...

    async def create_table(self, conn: None | Connection = None) -> None:
        sql = f"""
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
        await self._db.execute(sql)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
