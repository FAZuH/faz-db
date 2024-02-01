from __future__ import annotations
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator
from warnings import filterwarnings

from aiomysql import connect, DictCursor, Warning

from vindicator import ErrorHandler

filterwarnings("ignore", category=Warning)


class DatabaseQuery:

    def __init__(self, user: str, password: str, database: str, retries: int = 0) -> None:
        self._user: str = user
        self._password: str = password
        self._database: str = database
        self._retries: int = retries

    async def execute_fetch(self, sql: str, params: None | tuple[Any, ...] | dict[Any, Any] = None) -> None | list[dict[str, Any]]:
        async with self.get_cursor() as curs:
            await ErrorHandler.retry_decorator(self._retries, Exception)(curs.execute)(sql, params)
            return await curs.fetchall()

    async def execute(self, sql: str, params: None | tuple[Any, ...] | dict[Any, Any] = None) -> int:
        async with self.get_cursor() as curs:
            await ErrorHandler.retry_decorator(self._retries, Exception)(curs.execute)(sql, params)
            return curs.rowcount or 0

    def transaction_group(self):
        return _TransactionGroupContextManager(self)

    @asynccontextmanager
    async def get_cursor(self) -> AsyncGenerator[DictCursor, None]:
        async with connect(user=self._user, password=self._password, db=self._database) as conn:
            async with conn.cursor(DictCursor) as curs:
                yield curs

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
        async with self._parent.get_cursor() as curs:
            for q, p in self._sql:
                if p:
                    await ErrorHandler.retry_decorator(self._parent.retries, Exception)(curs.executemany)(q, p)
                else:
                    await ErrorHandler.retry_decorator(self._parent.retries, Exception)(curs.execute)(q)

    def add(self, sql: str, params: None | tuple[Any, ...] | dict[Any, Any] = None) -> None:
        self._sql.append((sql, params))

