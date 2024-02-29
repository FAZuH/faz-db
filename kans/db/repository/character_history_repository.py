from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

from . import Repository
from ..model import CharacterHistory, CharacterHistoryId

if TYPE_CHECKING:
    from aiomysql import Connection
    from kans.db import DatabaseQuery
    from kans.util import DbModelDictAdapter, DbModelIdDictAdapter


class CharacterHistoryRepository(Repository[CharacterHistory, CharacterHistoryId]):

    _TABLE_NAME: str = "character_history"

    def __init__(
        self,
        db: DatabaseQuery,
        db_model_dict_adapter: DbModelDictAdapter,
        db_model_id_dict_adapter: DbModelIdDictAdapter
    ) -> None:
        super().__init__(db)
        self._adapt = db_model_dict_adapter.from_character_history
        self._adapt_id = db_model_id_dict_adapter.from_character_history

    async def insert(self, entities: Iterable[CharacterHistory], conn: None | Connection = None) -> int:
        SQL = f"""
            INSERT IGNORE INTO `{self.table_name}` (
                `character_uuid`, `level`, `xp`, `wars`, `playtime`, `mobs_killed`, `chests_found`, `logins`,
                `deaths`, `discoveries`, `gamemode`, `alchemism`, `armouring`, `cooking`, `jeweling`, `scribing`,
                `tailoring`, `weaponsmithing`, `woodworking`, `mining`, `woodcutting`, `farming`, `fishing`,
                `dungeon_completions`, `quest_completions`, `raid_completions`, `datetime`
            )
            VALUES (
                %(character_uuid)s, %(level)s, %(xp)s, %(wars)s, %(playtime)s, %(mobs_killed)s, %(chests_found)s, %(logins)s,
                %(deaths)s, %(discoveries)s, %(gamemode)s, %(alchemism)s, %(armouring)s, %(cooking)s, %(jeweling)s, %(scribing)s,
                %(tailoring)s, %(weaponsmithing)s, %(woodworking)s, %(mining)s, %(woodcutting)s, %(farming)s, %(fishing)s,
                %(dungeon_completions)s, %(quest_completions)s, %(raid_completions)s, %(datetime)s
            )
        """
        return await self._db.execute_many(SQL, tuple(self._adapt(entity) for entity in entities), conn)

    async def exists(self, id_: CharacterHistoryId, conn: None | Connection = None) -> bool:
        SQL = f"SELECT COUNT(*) AS count FROM `{self.table_name}` WHERE `character_uuid` = %(character_uuid)s AND `character_uuid` = %(character_uuid)s"
        result = await self._db.fetch(SQL, self._adapt_id(id_), connection=conn)
        return result[0].get("count", 0) > 0

    async def count(self, conn: None | Connection = None) -> float:
        SQL = f"SELECT COUNT(*) AS count FROM `{self.table_name}`"
        result =await self._db.fetch(SQL, connection=conn)
        return result[0].get("count", 0)

    async def find_one(self, id_: CharacterHistoryId, conn: None | Connection = None) -> None | CharacterHistory:
        SQL = f"SELECT * FROM `{self.table_name}` WHERE `character_uuid` = %(character_uuid)s AND `datetime` = %(datetime)s"
        result = await self._db.fetch(SQL, self._adapt_id(id_), conn)
        return CharacterHistory(**result[0]) if result else None

    async def find_all(self, conn: None | Connection = None) -> list[CharacterHistory]:
        SQL = f"SELECT * FROM `{self.table_name}`"
        result = await self._db.fetch(SQL, connection=conn)
        return [CharacterHistory(**row) for row in result] if result else []

    async def update(self, entities: Iterable[CharacterHistory], conn: None | Connection = None) -> int:
        SQL = f"""
            UPDATE `{self.table_name}`
            SET `alchemism` = %(alchemism)s, `armouring` = %(armouring)s, `cooking` = %(cooking)s, `farming` = %(farming)s,
                `fishing` = %(fishing)s, `jeweling` = %(jeweling)s, `mining` = %(mining)s, `scribing` = %(scribing)s,
                `tailoring` = %(tailoring)s, `weaponsmithing` = %(weaponsmithing)s, `woodcutting` = %(woodcutting)s,
                `woodworking` = %(woodworking)s, `chests_found` = %(chests_found)s, `deaths` = %(deaths)s,
                `discoveries` = %(discoveries)s, `level` = %(level)s, `logins` = %(logins)s, `mobs_killed` = %(mobs_killed)s,
                `playtime` = %(playtime)s, `wars` = %(wars)s, `xp` = %(xp)s, `dungeon_completions` = %(dungeon_completions)s,
                `quest_completions` = %(quest_completions)s, `raid_completions` = %(raid_completions)s, `gamemode` = %(gamemode)s
            WHERE `character_uuid` = %(character_uuid)s AND `datetime` = %(datetime)s
        """
        return await self._db.execute_many(SQL, tuple(self._adapt(entity) for entity in entities), conn)

    async def delete(self, id_: CharacterHistoryId, conn: None | Connection = None) -> int:
        SQL = f"DELETE FROM `{self.table_name}` WHERE `character_uuid` = %(character_uuid)s AND `datetime` = %(datetime)s"
        return await self._db.execute(SQL, self._adapt_id(id_), conn)

    async def create_table(self, conn: None | Connection = None) -> None:
        SQL = f"""
            CREATE TABLE `{self.table_name}` (
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
                UNIQUE KEY `characterHistory_uq_ChuuidDt` (`character_uuid`,`datetime`),
                KEY `characterHistory_idx_ChuuidDt` (`character_uuid`,`datetime` DESC)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(SQL, connection=conn)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
