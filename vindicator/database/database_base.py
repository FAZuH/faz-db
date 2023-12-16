from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeAlias
from warnings import filterwarnings

import aiomysql
from aiomysql import Warning, connect

Record: TypeAlias = Dict[str, Any]
lRecords: TypeAlias = List[Record]


filterwarnings('ignore', category=Warning)


class DatabaseBase(ABC):

    @classmethod
    async def read_all(cls, query: str, params: Optional[dict] = None) -> lRecords:
        async with connect(user=cls.user(), password=cls.password(), db=cls.database()) as connection:
            connection: aiomysql.Connection
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                cursor: aiomysql.DictCursor
                await cursor.execute(query, params)
                return await cursor.fetchall()

    @classmethod
    async def read_many(cls, query: str, args: List[dict]) -> lRecords:
        async with connect(user=cls.user(), password=cls.password(), db=cls.database()) as connection:
            connection: aiomysql.Connection
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                cursor: aiomysql.DictCursor
                ret: lRecords = []

                for arg in args:
                    await cursor.execute(query, arg)
                    result: lRecords = await cursor.fetchall()
                    if result:
                        ret.append(result[0])
                return ret

    @classmethod
    async def write(cls, query: str, params: Optional[dict] = None) -> None:
        async with connect(user=cls.user(), password=cls.password(), db=cls.database()) as connection:
            connection: aiomysql.Connection
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                cursor: aiomysql.Cursor
                await cursor.execute(query, params)
                await connection.commit()

    @classmethod
    async def write_many(cls, query: str, seq_of_params: List[dict]) -> None:
        async with connect(user=cls.user(), password=cls.password(), db=cls.database()) as connection:
            connection: aiomysql.Connection
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                cursor: aiomysql.Cursor
                await cursor.executemany(query, seq_of_params)
                await connection.commit()

    @classmethod
    @abstractmethod
    def user(cls) -> str:
        ...

    @classmethod
    @abstractmethod
    def password(cls) -> str:
        ...

    @classmethod
    @abstractmethod
    def database(cls) -> str:
        ...
