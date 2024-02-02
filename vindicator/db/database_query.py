from __future__ import annotations
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any, AsyncGenerator, Iterable
from warnings import filterwarnings

from aiomysql import connect, DictCursor, Warning

from vindicator import ErrorHandler

if TYPE_CHECKING:
    from aiomysql import Connection

filterwarnings("ignore", category=Warning)


class DatabaseQuery:

    def __init__(self, user: str, password: str, database: str, retries: int = 0) -> None:
        self._user: str = user
        self._password: str = password
        self._database: str = database
        self._retries: int = retries

    async def fetch(
        self,
        sql: str,
        params: None | tuple[Any, ...] | dict[str, Any] = None,
        connection: None | Connection = None
    ) -> list[dict[str, Any]]:
        async with self.get_cursor(connection) as curs:
            await curs.execute(sql, params)
            return await curs.fetchall()

    async def fetch_many(
        self,
        sql: str,
        params: None | Iterable[tuple[Any, ...]] | Iterable[dict[str, Any]] = None,
        connection: None | Connection = None
    ) -> list[dict[str, Any]]:
        async with self.get_cursor(connection) as curs:
            await curs.executemany(sql, params)
            return await curs.fetchall()

    async def execute(
            self,
            sql: str,
            params: None | tuple[Any, ...] | dict[str, Any] = None,
            connection: None | Connection = None
    ) -> int:
        async with self.get_cursor(connection) as curs:
            await curs.execute(sql, params)
            return curs.rowcount or 0

    async def execute_many(
        self,
        sql: str,
        params: None | Iterable[tuple[Any, ...]] | Iterable[dict[str, Any]] = None,
        connection: None | Connection = None
    ) -> int:
        async with self.get_cursor(connection) as curs:
            await curs.executemany(sql, params)
            return curs.rowcount or 0

    def transaction_group(self) -> _TransactionGroupContextManager:
        return _TransactionGroupContextManager(self)

    @asynccontextmanager
    async def get_cursor(self, conn: None | Connection) -> AsyncGenerator[DictCursor, Any]:
        if conn:
            async with conn.cursor(DictCursor) as curs:
                yield curs
        else:
            async with self.get_connection() as conn:
                async with conn.cursor(DictCursor) as curs:
                    yield curs

    @asynccontextmanager
    async def get_connection(self) -> AsyncGenerator[Connection, Any]:
        conn: Connection
        async with connect(user=self._user, password=self._password, db=self._database, autocommit=True) as conn:
            yield conn
            await conn.commit()

    @property
    def user(self) -> str:
        return self._user

    @property
    def password(self) -> str:
        return self._password

    @property
    def database(self) -> str:
        return self._database

    @property
    def retries(self) -> int:
        return self._retries


class _TransactionGroupContextManager:

    def __init__(self, parent: DatabaseQuery) -> None:
        self._parent: DatabaseQuery = parent
        self._sql: list[tuple[str, None | tuple[Any, ...] | dict[Any, Any]]] = []

    async def __aenter__(self) -> _TransactionGroupContextManager:
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        conn: Connection
        curs: DictCursor
        async with connect(user=self._parent.user, password=self._parent.password, db=self._parent.database) as conn:
            async with conn.cursor(DictCursor) as curs:
                for q, p in self._sql:
                    if p:
                        await ErrorHandler.retry_decorator(self._parent.retries, Exception)(curs.executemany)(q, p)
                    else:
                        await ErrorHandler.retry_decorator(self._parent.retries, Exception)(curs.execute)(q)
            await conn.commit()

    def add(self, sql: str, params: None | tuple[Any, ...] | dict[Any, Any] = None) -> None:
        self._sql.append((sql, params))
