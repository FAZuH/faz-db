# pyright: reportPrivateUsage=none
from copy import deepcopy
from datetime import datetime
import unittest
from uuid import UUID

from loguru import logger

from kans import config
from kans.api.wynn.model.field import HeaderDateField
from kans.api.wynn.model.field import UsernameOrUuidField
from kans.db import KansDatabase
from kans.db.model import DateColumn, PlayerActivityHistory, PlayerActivityHistoryId
from kans.util import ApiResponseAdapter
from tests.fixtures_api import FixturesApi


class TestPlayerActivityHistoryRepository(unittest.IsolatedAsyncioTestCase):
    # self.repo to access repo
    # self.test_data to access test data

    async def asyncSetUp(self) -> None:
        self._adapter = ApiResponseAdapter()
        self._db = KansDatabase(config, logger)
        self._repo = self._db.player_activity_history_repository

        self._repo._TABLE_NAME = "test_player_activity_history"
        await self._repo.create_table()

        testData = self._get_data()
        self._testData1 = testData[0]
        self._testData2 = testData[1]

    async def test_create_table(self) -> None:
        # ACT
        await self._repo.create_table()

        # ASSERT
        # NOTE: Assert if the table exists
        res = await self._repo._db.fetch(f"SHOW TABLES LIKE '{self._repo._TABLE_NAME}'")
        self.assertEquals(self._repo.table_name, next(iter(res[0].values())))

    async def test_insert(self) -> None:
        # ACT
        n = await self._repo.insert(self._testData1)

        # ASSERT
        # NOTE: Assert if new players are inserted properly
        self.assertEquals(10, n)

        # ACT
        n = await self._repo.insert(self._testData2)

        # ASSERT
        # NOTE: Assert if new players are inserted properly
        self.assertEquals(15, len(await self._repo.find_all()))

    async def test_exists(self) -> None:
        # PREPARE
        await self._repo.insert(self._testData1)

        # ACT
        exists = [await self._repo.exists(PlayerActivityHistoryId(e.uuid, e.logon_datetime)) for e in self._testData1]

        # ASSERT
        # NOTE: Assert if the number of existing entities is the same as the inserted entities
        self.assertEquals(len(self._testData1), len(exists))
        # NOTE: Assert if all the entities exist
        self.assertTrue(all(exists))

    async def test_count(self) -> None:
        # PREPARE
        await self._repo.insert(self._testData1)

        # ACT
        count = await self._repo.count()

        # ASSERT
        # NOTE: Assert if the number of inserted entities is the same as the count
        self.assertEquals(len(self._testData1), count)

    async def test_find_one(self) -> None:
        # PREPARE
        await self._repo.insert(self._testData1)

        # ACT
        found: list[PlayerActivityHistory] = []
        for e in self._testData1:
            # Find the inserted e
            res = await self._repo.find_one(PlayerActivityHistoryId(e.uuid, e.logon_datetime))
            if res is not None:
                found.append(res)

        # ASSERT
        found_uuids = {e.uuid.uuid for e in found}
        test_uuids = {e.uuid.uuid for e in self._testData1}
        # NOTE: Assert if the number of found entities is the same as the inserted entities
        self.assertEquals(len(self._testData1), len(found))
        # NOTE: Assert if the found entities are the same as the inserted entities
        self.assertSetEqual(found_uuids, test_uuids)

    async def test_find_all(self) -> None:
        # PREPARE
        await self._repo.insert(self._testData1)

        # ACT
        found = await self._repo.find_all()

        # ASSERT
        found_uuids = {e.uuid.uuid for e in found}
        test_uuids = {e.uuid.uuid for e in self._testData1}
        # NOTE: Assert if the number of found entities is the same as the inserted entities
        self.assertEquals(len(self._testData1), len(found))
        # NOTE: Assert if the found entities are the same as the inserted entities
        self.assertSetEqual(found_uuids, test_uuids)

    async def test_update(self) -> None:
        # PREPARE
        await self._repo.insert(self._testData1)
        testDatetime1 = DateColumn(datetime.fromtimestamp(1_709_181_095))
        for e in self._testData1:
            e._logoff_datetime = testDatetime1

        # ACT
        n = await self._repo.update(self._testData1)

        # ASSERT
        # NOTE: Assert if the number of updated entities is correct
        self.assertEquals(len(self._testData1), n)
        for e in (await self._repo.find_all()):
            # NOTE: Assert if the updated e is the same as the updated values
            self.assertEquals(testDatetime1.datetime, e.logoff_datetime.datetime)

    async def test_delete(self) -> None:
        # PREPARE
        await self._repo.insert(self._testData1)

        # ACT
        n = await self._repo.delete(PlayerActivityHistoryId(self._testData1[0].uuid, self._testData1[0].logon_datetime))

        # PREPARE
        found = await self._repo.find_all()

        # ASSERT
        # NOTE: Assert if the number of deleted entities is correct
        self.assertEquals(1, n)
        # NOTE: Assert if the number of found entities is correct
        self.assertEquals(len(self._testData1) - 1, len(found))


    async def asyncTearDown(self) -> None:
        await self._repo._db.execute(f"DROP TABLE IF EXISTS `{self._repo._TABLE_NAME}`")
        return


    def _get_data(self) -> tuple[list[PlayerActivityHistory], list[PlayerActivityHistory]]:
        testDatetime1 = datetime.fromtimestamp(1_709_181_095)
        testDatetime2 = datetime.fromtimestamp(1_709_181_195)  # + 100
        testDatetime3 = datetime.fromtimestamp(1_709_180_095)  # - 1000
        testDatetime4 = datetime.fromtimestamp(1_709_180_095)  # - 1000
        testOnlinePlayers1 = {
                UsernameOrUuidField(str(UUID(int=i + 1))): ''
                for i in range(10)
        }
        testOnlinePlayers2 = {
                UsernameOrUuidField(str(UUID(int=i + 1))): ''
                for i in range(5, 15)
        }

        fixtures = FixturesApi()
        resp = fixtures.get_online_uuids()

        resp1  = deepcopy(resp)
        resp2 = deepcopy(resp)

        resp1.body._players = testOnlinePlayers1
        resp2.body._players = testOnlinePlayers2
        resp1.headers._expires = HeaderDateField(testDatetime1.isoformat())
        resp1.headers._expires = HeaderDateField(testDatetime2.isoformat())

        raw_test_data1 = list(self._adapter.OnlinePlayers.to_player_activity_history(
                resp1, {uuid.username_or_uuid: testDatetime3 for uuid in resp1.body.players}  # type: ignore
        ))
        raw_test_data2 = list(self._adapter.OnlinePlayers.to_player_activity_history(
                resp2, {uuid.username_or_uuid: testDatetime4 for uuid in resp2.body.players}  # type: ignore
        ))

        self.assertEquals(10, len(raw_test_data1))
        self.assertEquals(10, len(raw_test_data2))
        return raw_test_data1, raw_test_data2
