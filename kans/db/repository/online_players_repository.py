from __future__ import annotations
from typing import TYPE_CHECKING, Any, Iterable

from kans import OnlinePlayers, Repository

if TYPE_CHECKING:
    from aiomysql import Connection
    from kans import DatabaseQuery


class OnlinePlayersRepository(Repository[OnlinePlayers]):

    _TABLE_NAME = "online_players"

    def __init__(self, db: DatabaseQuery) -> None:
        self._db = db

    async def insert(self, entities: Iterable[OnlinePlayers], conn: None | Connection = None) -> int:
        async with self._db.transaction_group() as tg:
            tg.add(f"DELETE FROM `{self.table_name}` WHERE `uuid` IS NOT NULL")
            tg.add(
                f"INSERT INTO `{self.table_name}` (`uuid`, `server`) VALUES (%s, %s)",
                tuple((entity.uuid.uuid, entity.server) for entity in entities)
            )
        return 0

    async def exists(self,id_: Any, conn: None | Connection = None) -> bool: ...

    async def count(self, conn: None | Connection = None) -> float:
        sql = f"SELECT COUNT(*) FROM `{self.table_name}`"
        return (await self._db.fetch(sql, connection=conn))[0].get("COUNT(*)", 0)

    async def find_one(self, id_: Any, conn: None | Connection = None) -> None | OnlinePlayers: ...

    async def find_all(self, conn: None | Connection = None) -> None | list[OnlinePlayers]: ...

    async def update(self, entities: Iterable[OnlinePlayers], conn: None | Connection = None) -> int: ...

    async def delete(self, id_: Any, conn: None | Connection = None) -> int: ...

    async def create_table(self, conn: None | Connection = None) -> None:
        sql = f"""
        CREATE TABLE IF NOT EXISTS `{self.table_name}` (
            `uuid` binary(16) NOT NULL,
            `server` varchar(10) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        await self._db.execute(sql)

    @property
    def table_name(self) -> str:
        return self._TABLE_NAME
