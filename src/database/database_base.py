import aiomysql
from typing import Optional, TypeVar, Type, TYPE_CHECKING

import asyncio_atexit

if TYPE_CHECKING:
    from .vindicator_database import VindicatorDatabase

T = TypeVar("T", bound="VindicatorDatabase")


class DatabaseBase:
    _connection: Optional[aiomysql.Connection]

    @staticmethod
    async def _ainit(pcls: Type[T]):  # pcls is the subclass
        pcls._connection = await aiomysql.connect(user="root", password="root", db=pcls._database)
        asyncio_atexit.register(pcls._close_connection)

    @classmethod
    async def _close_connection(cls):
        await cls._connection.commit()
        await cls._connection.close()

    @classmethod
    async def read_all(cls, query, params=None) -> dict:
        async with cls._connection.cursor(aiomysql.DictCursor) as cursor:
            cursor: aiomysql.DictCursor
            await cursor.execute(query, params)
            return await cursor.fetchall()

    @classmethod
    async def write(cls, query, params=None):
        async with cls._connection.cursor() as cursor:
            cursor: aiomysql.Cursor
            await cursor.execute(query, params)
            await cls._connection.commit()

    @classmethod
    async def write_many(cls, query, seq_of_params):
        async with cls._connection.cursor() as cursor:
            cursor: aiomysql.Cursor
            await cursor.executemany(query, seq_of_params)
            await cls._connection.commit()
