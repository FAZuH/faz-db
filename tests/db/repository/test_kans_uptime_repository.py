# pyright: reportPrivateUsage=none
from datetime import datetime, timedelta
from unittest.mock import MagicMock
import unittest

from wynndb import Config
from wynndb.adapter import ApiResponseAdapter
from wynndb.db import KansDatabase
from wynndb.db.wynndb.model import KansUptime, KansUptimeId


class TestKansUptimeRepository(unittest.IsolatedAsyncioTestCase):
    # self.repo to access repo
    # self.test_data to access test data

    async def asyncSetUp(self) -> None:
        self._adapter = ApiResponseAdapter()
        self._db = KansDatabase(Config(), MagicMock())
        self._repo = self._db.kans_uptime_repository

        self._repo._TABLE_NAME = "test_kans_uptime"
        await self._repo.create_table()

        self._testData = self._get_data()


    async def test_create_table(self) -> None:
        # ACT
        await self._repo.create_table()

        # ASSERT
        # NOTE: Assert if the table exists
        res = await self._repo._db.fetch(f"SHOW TABLES LIKE '{self._repo._TABLE_NAME}'")
        self.assertEquals(self._repo.table_name, next(iter(res[0].values())))

    async def test_insert(self) -> None:
        # ACT
        await self._repo.insert(self._testData)

        # ASSERT
        # NOTE: Assert if the number of inserted entities is correct
        res = await self._db.query.fetch(f"SELECT * FROM {self._repo.table_name}")
        self.assertEquals(2, len(res))

    async def test_exists(self) -> None:
        # PREPARE
        await self._repo.insert(self._testData)

        # ACT
        exists = [
                await self._repo.exists(KansUptimeId(e.start_time))
                for e in self._testData
        ]

        # ASSERT
        # NOTE: Assert if the number of existing entities is the same as the inserted entities
        self.assertEquals(len(self._testData), len(exists))
        # NOTE: Assert if all the entities exist
        self.assertTrue(all(exists))

    async def test_count(self) -> None:
        # PREPARE
        await self._repo.insert(self._testData)

        # ACT
        count = await self._repo.count()

        # ASSERT
        # NOTE: Assert if the number of inserted entities is the same as the count
        self.assertEquals(2, count)

    async def test_find_one(self) -> None:
        # PREPARE
        await self._repo.insert(self._testData)

        # ACT
        found: list[KansUptime] = []
        for e in self._testData:
            # Find the inserted e
            res = await self._repo.find_one(KansUptimeId(e.start_time))
            if res is not None:
                found.append(res)

        # ASSERT
        found_time = {e.start_time.datetime for e in found}
        test_time = {e.start_time.datetime for e in self._testData}
        # NOTE: Assert if the number of found entities is the same as the inserted entities
        self.assertEquals(len(self._testData), len(found))
        # NOTE: Assert if the found entities are the same as the inserted entities
        self.assertSetEqual(found_time, test_time)

    async def test_find_all(self) -> None:
        # PREPARE
        await self._repo.insert(self._testData)

        # ACT
        found = await self._repo.find_all()

        # ASSERT
        found_time = {e.start_time.datetime for e in found}
        test_time = {e.start_time.datetime for e in self._testData}
        # NOTE: Assert if the number of found entities is the same as the inserted entities
        self.assertEquals(2, len(found))
        # NOTE: Assert if the found entities are the same as the inserted entities
        self.assertSetEqual(found_time, test_time)

    async def test_update(self) -> None:
        # PREPARE
        temp = self._testData[0]
        testDatetime1 = temp.start_time.datetime + timedelta(days=1)
        testDatum = KansUptime(temp.start_time, testDatetime1)
        await self._repo.insert(self._testData)

        # ACT
        n = await self._repo.update((testDatum,))

        # ASSERT
        # NOTE: Assert if the number of updated entities is correct
        self.assertEquals(1, n)
        res = await self._repo.find_one(KansUptimeId(temp.start_time))
        self.assertIsNotNone(res)
        # NOTE: Assert if the updated e is the same as the updated values
        self.assertEquals(testDatetime1, res.stop_time.datetime)  # type: ignore

    async def test_delete(self) -> None:
        # PREPARE
        await self._repo.insert(self._testData)

        # ACT
        n = await self._repo.delete(KansUptimeId(self._testData[0].start_time))

        # PREPARE
        found = await self._repo.find_all()

        # ASSERT
        # NOTE: Assert if the number of deleted entities is correct
        self.assertEquals(1, n)
        # NOTE: Assert if the number of found entities is correct
        self.assertEquals(1, len(found))


    async def asyncTearDown(self) -> None:
        await self._repo._db.execute(f"DROP TABLE IF EXISTS `{self._repo._TABLE_NAME}`")
        return


    def _get_data(self) -> list[KansUptime]:
        testTimestamp1 = 1709181095
        testData: list[KansUptime] = [
                KansUptime(
                        start_time=datetime.fromtimestamp(testTimestamp1),
                        stop_time=datetime.fromtimestamp(testTimestamp1 + i)
                )
                for i in range(5)
        ]
        testData.extend(
                KansUptime(
                        start_time=datetime.fromtimestamp(testTimestamp1 + 10),
                        stop_time=datetime.fromtimestamp(testTimestamp1 + i)
                )
                for i in range(5)
        )
        return testData
