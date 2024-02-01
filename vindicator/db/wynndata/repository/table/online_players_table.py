from __future__ import annotations
from typing import TYPE_CHECKING
from typing_extensions import override, Iterable

from vindicator import OnlinePlayersRepo

if TYPE_CHECKING:
    from aiomysql import Connection
    from vindicator import (
        DatabaseQuery,
        OnlinePlayers,
        OnlinePlayersId
    )


class OnlinePlayersTable(OnlinePlayersRepo):

    _TABLE_NAME: str = "online_players"

    def __init__(self, db: DatabaseQuery) -> None:
        self._db = db

    @override
    async def insert(self, connection: None | Connection, entity: Iterable[OnlinePlayers]) -> bool:
        async with self._db.transaction_group() as tg:
            tg.add(f"DELETE FROM {self.table_name} WHERE uuid IS NOT NULL")
            tg.add(
                f"INSERT INTO {self.table_name} (uuid, server) VALUES (%s, %s)",
                (entity.uuid, entity.server)
            )
        return True

    async def exists(self, id_: OnlinePlayersId) -> bool: ...

    async def count(self) -> float: ...

    async def find_one(self, id_: OnlinePlayersId) -> None | OnlinePlayers: ...

    async def find_all(self) -> None | list[OnlinePlayers]: ...

    async def update(self, entity: OnlinePlayers) -> bool: ...

    async def delete(self, id_: OnlinePlayersId) -> bool: ...

    async def create_table(self) -> None:
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
