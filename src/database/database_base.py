from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar
from warnings import filterwarnings

import aiomysql
import asyncio_atexit

if TYPE_CHECKING:
    from .vindicator_database import VindicatorDatabase

T = TypeVar("T", bound="VindicatorDatabase")

filterwarnings('ignore', category=aiomysql.Warning)


class DatabaseBase:

    _connection: Optional[aiomysql.Connection]

    @staticmethod
    async def _ainit(pcls: Type[T]):  # pcls is the subclass
        pcls._connection = await aiomysql.connect(user="root", password="root", db=pcls._database)  # type: ignore
        asyncio_atexit.register(pcls._close_connection)
        return

    @classmethod
    async def _close_connection(cls):
        if not cls._connection:
            raise RuntimeError("Database connection not established")

        await cls._connection.commit()
        cls._connection.close()
        return

    @classmethod
    async def read_all(cls, query: str, params: Optional[dict] = None) -> List[Dict[str, Any]]:
        if not cls._connection:
            raise RuntimeError("Database connection not established")


        async with cls._connection.cursor(aiomysql.DictCursor) as cursor:
            cursor: aiomysql.DictCursor
            await cursor.execute(query, params)
            return await cursor.fetchall()

    @classmethod
    async def write(cls, query: str, params: Optional[dict] = None) -> None:
        if not cls._connection:
            raise RuntimeError("Database connection not established")

        async with cls._connection.cursor() as cursor:
            cursor: aiomysql.Cursor
            await cursor.execute(query, params)
            await cls._connection.commit()

        return

    @classmethod
    async def write_many(cls, query: str, seq_of_params: List[dict]) -> None:
        if not cls._connection:
            raise RuntimeError("Database connection not established")

        async with cls._connection.cursor() as cursor:
            cursor: aiomysql.Cursor
            await cursor.executemany(query, seq_of_params)
            await cls._connection.commit()

        return
