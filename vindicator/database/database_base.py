from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional
from warnings import filterwarnings

from aiomysql import connect, DictCursor, Warning

from vindicator.utils.error_handler import ErrorHandler

if TYPE_CHECKING:
    from vindicator.types import *


filterwarnings("ignore", category=Warning)


class DatabaseBase(ABC):

    @classmethod
    async def read_all(cls, query: str, params: Optional[dict] = None) -> lRecords:
        async with connect(user=cls.user(), password=cls.password(), db=cls.database()) as conn:
            conn: Connection
            @ErrorHandler.aretry(times=cls.retries(), exceptions=Exception)
            async def _read_all() -> lRecords:
                async with conn.cursor(DictCursor) as curs:
                    curs: DictCursor
                    await curs.execute(query, params)
                    return await curs.fetchall()
            return await _read_all()

    @classmethod
    async def read_many(cls, query: str, args: List[dict]) -> lRecords:
        async with connect(user=cls.user(), password=cls.password(), db=cls.database()) as conn:
            conn: Connection
            @ErrorHandler.aretry(times=cls.retries(), exceptions=Exception)
            async def _read_many() -> lRecords:
                async with conn.cursor(DictCursor) as curs:
                    curs: DictCursor
                    ret: lRecords = []
                    for arg in args:
                        await curs.execute(query, arg)
                        res: lRecords = await curs.fetchall()
                        if res:
                            ret.append(res[0])
                return ret
            return await _read_many()

    @classmethod
    async def write(cls, query: str, params: Optional[dict] = None) -> None:
        async with connect(user=cls.user(), password=cls.password(), db=cls.database()) as conn:
            conn: Connection
            @ErrorHandler.aretry(times=cls.retries(), exceptions=Exception)
            async def _write() -> None:
                async with conn.cursor(DictCursor) as curs:
                    curs: Cursor
                    await curs.execute(query, params)
                    await conn.commit()
            await _write()
    @classmethod
    async def write_many(cls, query: str, seq_of_params: List[dict]) -> None:
        async with connect(user=cls.user(), password=cls.password(), db=cls.database()) as conn:
            conn: Connection
            @ErrorHandler.aretry(times=cls.retries(), exceptions=Exception)
            async def _write_many() -> None:
                async with conn.cursor(DictCursor) as curs:
                    curs: Cursor
                    await curs.executemany(query, seq_of_params)
                    await conn.commit()
            await _write_many()

    @classmethod
    @abstractmethod
    def database(cls) -> str:
        ...

    @classmethod
    @abstractmethod
    def password(cls) -> str:
        ...

    @classmethod
    @abstractmethod
    def retries(cls) -> int:
        ...

    @classmethod
    @abstractmethod
    def user(cls) -> str:
        ...
