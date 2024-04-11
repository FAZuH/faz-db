from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, Generic, Iterable, TypeVar

T = TypeVar('T')
ID = TypeVar('ID')

if TYPE_CHECKING:
    from decimal import Decimal
    from aiomysql import Connection
    from ... import DatabaseQuery


class Repository(ABC, Generic[T]):
    """Abstract class for a repository.

    Args:
        `Generic[T]`: The type of the entity.
    """

    def __init__(self, db: DatabaseQuery, adapter: Callable[[T], Any]) -> None:
        self._db = db
        self._adapt = adapter

    async def table_size(self, conn: None | Connection = None) -> Decimal:
        SQL = f"""
            SELECT
                ROUND(((data_length + index_length)), 2) AS "size_bytes"
            FROM
                information_schema.TABLES
            WHERE
                table_schema = '{self._db.database}'
                AND table_name = '{self.table_name}';
        """
        res = await self._db.fetch(SQL, connection=conn)
        return res[0].get("size_bytes", 0)

    @abstractmethod
    async def insert(self, entities: Iterable[T], conn: None | Connection = None) -> int: ...

    @abstractmethod
    async def create_table(self, conn: None | Connection = None) -> None: ...

    @property
    @abstractmethod
    def table_name(self) -> str: ...
