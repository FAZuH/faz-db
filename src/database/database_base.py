from typing import TYPE_CHECKING, Iterable, List, Optional, Type

import asyncio_atexit

if TYPE_CHECKING:
    from pathlib import Path


class DatabaseBase:
    _connection: aiosqlite.Connection
    _directory: 'Path'

    @staticmethod
    async def _init_class_attrs(cls: Type[T]) -> None:  # pcls is the subclass, hence staticmethod
        cls._connection = await aiosqlite.connect(cls._directory)
        cls._connection.row_factory = Row
        asyncio_atexit.register(cls._close_connection)

    @classmethod
    async def readall(cls, query: str, params: Optional[List] = None) -> Iterable[Row]:
        cursor = await cls._connection.cursor()
        await cursor.execute(query, params)
        return await cursor.fetchall()

    @classmethod
    async def write(cls, query: str, params: Optional[List] = None) -> None:
        cursor = await cls._connection.cursor()
        await cursor.execute(query, params)
        await cls._connection.commit()

    @classmethod
    async def writemany(cls, query: str, seq_of_params: List) -> None:
        cursor = await cls._connection.cursor()
        await cursor.executemany(query, seq_of_params)
        await cls._connection.commit()

    @classmethod
    async def _close_connection(cls) -> None:
        await cls._connection.commit()
        await cls._connection.close()
