from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

from . import Repository
from ..model import OnlinePlayers, OnlinePlayersId

if TYPE_CHECKING:
    from aiomysql import Connection
    from kans.db import DatabaseQuery
    from kans.util import DbModelDictAdapter, DbModelIdDictAdapter


class OnlinePlayersRepository(Repository[OnlinePlayers, OnlinePlayersId]):

    _TABLE_NAME = "online_players"

    def __init__(
        self,
        db: DatabaseQuery,
        db_model_dict_adapter: DbModelDictAdapter,
        db_model_id_dict_adapter: DbModelIdDictAdapter
    ) -> None:
        super().__init__(db)
        self._adapt = db_model_dict_adapter.from_online_players
        self._adapt_id = db_model_id_dict_adapter.from_online_players

    async def insert(self, entities: Iterable[OnlinePlayers], conn: None | Connection = None) -> int:
        async with self._db.transaction_group() as tg:
            tg.add(f"DELETE FROM `{self.table_name}` WHERE `uuid` IS NOT NULL")
            tg.add(
                    f"INSERT INTO `{self.table_name}` (`uuid`, `server`) VALUES (%(uuid)s, %(server)s)",
                    tuple(self._adapt(entity) for entity in entities)
            )
        return 0

    async def exists(self, id_: OnlinePlayersId, conn: None | Connection = None) -> bool:
        SQL = f"SELECT COUNT(*) AS count FROM `{self.table_name}` WHERE `uuid` = %(uuid)s"
        result = await self._db.fetch(SQL, self._adapt_id(id_), connection=conn)
        return result[0].get("count", 0) > 0

    async def count(self, conn: None | Connection = None) -> float:
        SQL = f"SELECT COUNT(*) FROM `{self.table_name}`"
        return (await self._db.fetch(SQL, connection=conn))[0].get("COUNT(*)", 0)

    async def find_one(self, id_: OnlinePlayersId, conn: None | Connection = None) -> None | OnlinePlayers:
        SQL = f"SELECT * FROM `{self.table_name}` WHERE `uuid` = %(uuid)s"
        result = await self._db.fetch(SQL, self._adapt_id(id_), connection=conn)
        return OnlinePlayers(**result[0]) if result else None

    async def find_all(self, conn: None | Connection = None) -> list[OnlinePlayers]:
        SQL = f"SELECT * FROM `{self.table_name}`"
        result = await self._db.fetch(SQL, connection=conn)
        return [OnlinePlayers(**row) for row in result] if result else []

    async def update(self, entities: Iterable[OnlinePlayers], conn: None | Connection = None) -> int:
        SQL = f"""
            UPDATE `{self.table_name}`
            SET `server` = %(server)s
            WHERE `uuid` = %(uuid)s
        """
        return await self._db.execute_many(SQL, tuple(self._adapt(entity) for entity in entities), conn)

    async def delete(self, id_: OnlinePlayersId, conn: None | Connection = None) -> int: ...

    async def create_table(self, conn: None | Connection = None) -> None:
        SQL = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                `uuid` binary(16) NOT NULL,
                `server` varchar(10) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(SQL)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
