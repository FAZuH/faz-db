# pyright: reportPrivateUsage=none
from datetime import datetime
import unittest

from wynndb.config import Config
from wynndb.db import WynnDbDatabase
from wynndb.db.wynndb.model import WynnDbUptime
from wynndb.logger.wynndb_logger import WynnDbLogger
from wynndb.util import ApiResponseAdapter


class TestWynnDbUptimeRepository(unittest.IsolatedAsyncioTestCase):
    # self.repo to access repo
    # self.test_data to access test data

    async def asyncSetUp(self) -> None:
        Config.load_config()
        self._adapter = ApiResponseAdapter()
        self._db = WynnDbDatabase(WynnDbLogger())
        self._repo = self._db.wynndb_uptime_repository

        self._repo._TABLE_NAME = "test_wynndb_uptime"
        await self._repo.create_table()

        self._testData = self._get_data()


    async def test_create_table(self) -> None:
        # ACT
        await self._repo.create_table()

        # ASSERT
        # NOTE: Assert if the table exists
        res = await self._repo._db.fetch(f"SHOW TABLES LIKE '{self._repo._TABLE_NAME}'")
        self.assertEqual(self._repo.table_name, next(iter(res[0].values())))

    async def test_insert(self) -> None:
        # ACT
        await self._repo.insert(self._testData)

        # ASSERT
        # NOTE: Assert if the number of inserted entities is correct
        res = await self._db.query.fetch(f"SELECT * FROM {self._repo.table_name}")
        self.assertEqual(2, len(res))

    async def asyncTearDown(self) -> None:
        await self._repo._db.execute(f"DROP TABLE IF EXISTS `{self._repo._TABLE_NAME}`")
        return

    def _get_data(self) -> list[WynnDbUptime]:
        testTimestamp1 = 1709181095
        testData: list[WynnDbUptime] = [
                WynnDbUptime(
                        start_time=datetime.fromtimestamp(testTimestamp1),
                        stop_time=datetime.fromtimestamp(testTimestamp1 + i)
                )
                for i in range(5)
        ]
        testData.extend(
                WynnDbUptime(
                        start_time=datetime.fromtimestamp(testTimestamp1 + 10),
                        stop_time=datetime.fromtimestamp(testTimestamp1 + i)
                )
                for i in range(5)
        )
        return testData
