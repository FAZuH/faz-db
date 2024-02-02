from __future__ import annotations
from typing import TYPE_CHECKING, Iterable, Protocol, TypeVar

ID_contra = TypeVar('ID_contra', contravariant=True)
T = TypeVar('T')

if TYPE_CHECKING:
    from aiomysql import Connection
    optConn = None | Connection


class TableProtocol(Protocol[T, ID_contra]):
    """<<interface>>

    Generic[T, ID]
    """
    async def insert(self, entities: Iterable[T], conn: None | Connection = None) -> int: ...
    async def exists(self, id_: ID_contra, conn: None | Connection = None) -> bool: ...
    async def count(self, conn: None | Connection = None) -> float:
        sql = f"SELECT COUNT(*) FROM `{self.table_name}`"
        return (await self._db.fetch(sql, connection=conn))[0].get("COUNT(*)", 0)
    async def find_one(self, id_: ID_contra, conn: None | Connection = None) -> None | T: ...
    async def find_all(self, conn: None | Connection = None) -> None | list[T]: ...
    async def update(self, entities: Iterable[T], conn: None | Connection = None) -> int: ...
    async def delete(self, id_: ID_contra, conn: None | Connection = None) -> int: ...
    async def create_table(self, conn: None | Connection = None) -> None: ...
    @property
    def table_name(self) -> str: ...
