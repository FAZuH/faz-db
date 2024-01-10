from __future__ import annotations
from abc import ABC
from warnings import filterwarnings

from aiomysql import connect, DictCursor, Warning

from vindicator import ErrorHandler
from vindicator.typehints import *


filterwarnings("ignore", category=Warning)


class DatabaseBase(ABC):

    _DATABASE: str
    _PASSWORD: str
    _RETRIES: int
    _USER: str

    @classmethod
    async def execute(cls, query: str, params: Optional[Iterable[Union[dict, TypedDict]]] = []) -> Optional[List[Record]]:
        conn: Connection; curs: DictCursor
        async with cls.create_connection() as conn:
            async with conn.cursor(DictCursor) as curs:
                if params:
                    await ErrorHandler.retry_decorator(cls._RETRIES, Exception)(curs.executemany)(query, params)
                else:
                    await ErrorHandler.retry_decorator(cls._RETRIES, Exception)(curs.execute)(query)
                await conn.commit()
                return await curs.fetchall()

    @classmethod
    def transaction_group(cls):
        class _TransactionGroupContextManager:

            def __init__(self):
                self._query: List[Tuple[str, Iterable[Union[dict, TypedDict]]]] = []

            async def __aenter__(self) -> Self:
                return self

            async def __aexit__(self, exc_type: ExcTypeT, exc: ExcT, tb: TbT) -> None:
                conn: Connection; curs: DictCursor
                async with cls.create_connection() as conn:
                    async with conn.cursor(DictCursor) as curs:
                        for q, p in self._query:
                            if p:
                                await ErrorHandler.retry_decorator(cls._RETRIES, Exception)(curs.executemany)(q, p)
                            else:
                                await ErrorHandler.retry_decorator(cls._RETRIES, Exception)(curs.execute)(q)
                        await conn.commit()

            def add(self, query: str, params: Iterable[dict] = []) -> None:
                self._query.append((query, params))

        return _TransactionGroupContextManager()

    @classmethod
    def create_connection(cls):
        return connect(user=cls._USER, password=cls._PASSWORD, db=cls._DATABASE)
