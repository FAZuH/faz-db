from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from unittest import IsolatedAsyncioTestCase

from wynndb.config import Config
from wynndb.db import DatabaseQuery
from wynndb.util import ApiResponseAdapter

if TYPE_CHECKING:
    from wynndb.db.wynndb.repository import Repository


class BaseRepositoryTestCase[T](IsolatedAsyncioTestCase, ABC):

    def __init__(self, repository: type[Repository[T]], methodName: str) -> None:
        self._repo_type = repository
        super().__init__(methodName)

    # override
    async def asyncSetUp(self) -> None:
        Config.load_config()
        wynndb_query = DatabaseQuery(
            Config.get_db_username(),
            Config.get_db_password(),
            Config.get_schema_name(),
            Config.get_db_max_retries()
        )

        self._repo = self._repo_type(wynndb_query)
        self._repo._TABLE_NAME = f"test_{self._repo.table_name}"  # type: ignore
        await self._repo.create_table()

        self._adapter = ApiResponseAdapter()
        self._testData = self._get_data()

    # override
    async def asyncTearDown(self) -> None:
        await self._repo._db.execute(f"DROP TABLE IF EXISTS `{self._repo.table_name}`")

    async def assert_table_exists(self) -> None:
        res = await self._repo._db.fetch(f"SHOW TABLES LIKE '{self._repo.table_name}'")
        self.assertEqual(self._repo.table_name, next(iter(res[0].values())))

    @abstractmethod
    def _get_data(self) -> list[T]: ...

