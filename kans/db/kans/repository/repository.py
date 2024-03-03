from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING, Generic, Iterable, TypeVar

T = TypeVar('T')
ID = TypeVar('ID')

if TYPE_CHECKING:
    from decimal import Decimal
    from aiomysql import Connection
    from .. import DatabaseQuery


class Repository(ABC, Generic[T, ID]):
    """Abstract class for a repository.

    Args:
        `Generic[T, ID]`: The type of the entity and the type of the entity's id.
    """

    def __init__(self, db: DatabaseQuery) -> None:
        self._db = db

    async def insert(self, entities: Iterable[T], conn: None | Connection = None) -> int: ...

    async def exists(self, id_: ID, conn: None | Connection = None) -> bool: ...

    async def count(self, conn: None | Connection = None) -> float: ...

    async def find_one(self, id_: ID, conn: None | Connection = None) -> None | T: ...

    async def find_all(self, conn: None | Connection = None) -> list[T]: ...

    async def update(self, entities: Iterable[T], conn: None | Connection = None) -> int: ...

    async def delete(self, id_: ID, conn: None | Connection = None) -> int: ...

    async def create_table(self, conn: None | Connection = None) -> None: ...

    async def table_size(self, conn: None | Connection = None) -> Decimal:
        sql = f"""
            SELECT
                ROUND(((data_length + index_length)), 2) AS "size_bytes"
            FROM
                information_schema.TABLES
            WHERE
                table_schema = '{self._db.database}'
                AND table_name = '{self.table_name}';
        """
        res = await self._db.fetch(sql, connection=conn)
        return res[0].get("size_bytes", 0)

    @property
    def table_name(self) -> str: ...
