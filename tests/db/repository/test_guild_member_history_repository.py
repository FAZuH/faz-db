# pyright: reportPrivateUsage=none
from datetime import datetime
import unittest
from unittest.mock import MagicMock
from uuid import UUID

from wynndb import Config
from wynndb.adapter import ApiResponseAdapter
from wynndb.db import KansDatabase
from wynndb.db.wynndb.model import GuildMemberHistory, GuildMemberHistoryId
from tests.fixtures_api import FixturesApi


class TestGuildMemberHistoryRepository(unittest.IsolatedAsyncioTestCase):
    # self.repo to access repo
    # self.test_data to access test data

    async def asyncSetUp(self) -> None:
        self._adapter = ApiResponseAdapter()
        self._db = KansDatabase(Config(), MagicMock())
        self._repo = self._db.guild_member_history_repository

        self._repo._TABLE_NAME = "test_guild_member_history"
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
        n = await self._repo.insert(self._testData)

        # ASSERT
        # NOTE: Assert if the number of inserted entities is correct
        self.assertEquals(10, n)

        # PREPARE
        toTest1: list[GuildMemberHistory] = []
        testDatetime1 = datetime.fromtimestamp(1709181095)
        testUuid1 = UUID(int=69).bytes
        for e in self._testData:
            as_dict = self._repo._adapt(e)
            as_dict["uuid"] = testUuid1
            as_dict["datetime"] = testDatetime1
            toTest1.append(e.__class__(**as_dict))

        # ACT
        n = await self._repo.insert(toTest1)

        # ASSERT
        # NOTE: Assert unique constraints of character_uuid
        self.assertEquals(1, n)

    async def test_exists(self) -> None:
        # PREPARE
        await self._repo.insert(self._testData)

        # ACT
        exists = [
                await self._repo.exists(GuildMemberHistoryId(e.uuid, e.datetime))
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
        self.assertEquals(len(self._testData), count)

    async def test_find_one(self) -> None:
        # PREPARE
        await self._repo.insert(self._testData)

        # ACT
        found: list[GuildMemberHistory] = []
        for e in self._testData:
            # Find the inserted e
            res = await self._repo.find_one(GuildMemberHistoryId(e.uuid, e.datetime))
            if res is not None:
                found.append(res)

        # ASSERT
        found_uuid = {e.uuid.uuid for e in found}
        test_uuid = {e.uuid.uuid for e in self._testData}
        # NOTE: Assert if the number of found entities is the same as the inserted entities
        self.assertEquals(len(self._testData), len(found))
        # NOTE: Assert if the found entities are the same as the inserted entities
        self.assertSetEqual(found_uuid, test_uuid)

    async def test_find_all(self) -> None:
        # PREPARE
        await self._repo.insert(self._testData)

        # ACT
        found = await self._repo.find_all()

        # ASSERT
        found_uuid = {e.uuid.uuid for e in found}
        test_uuid = {e.uuid.uuid for e in self._testData}
        # NOTE: Assert if the number of found entities is the same as the inserted entities
        self.assertEquals(len(self._testData), len(found))
        # NOTE: Assert if the found entities are the same as the inserted entities
        self.assertSetEqual(found_uuid, test_uuid)

    async def test_update(self) -> None:
        # PREPARE
        testContributed1 = 10_000_000
        await self._repo.insert(self._testData)
        for e in self._testData:
            e._contributed = testContributed1

        # ACT
        n = await self._repo.update(self._testData)

        # ASSERT
        # NOTE: Assert if the number of updated entities is correct
        self.assertEquals(len(self._testData), n)
        for e in (await self._repo.find_all()):
            # NOTE: Assert if the updated e is the same as the updated values
            self.assertEquals(testContributed1, e.contributed)

    async def test_delete(self) -> None:
        # PREPARE
        await self._repo.insert(self._testData)

        # ACT
        n = await self._repo.delete(GuildMemberHistoryId(self._testData[0].uuid, self._testData[0].datetime))

        # PREPARE
        found = await self._repo.find_all()

        # ASSERT
        # NOTE: Assert if the number of deleted entities is correct
        self.assertEquals(1, n)
        # NOTE: Assert if the number of found entities is correct
        self.assertEquals(len(self._testData) - 1, len(found))


    async def asyncTearDown(self) -> None:
        await self._repo._db.execute(f"DROP TABLE IF EXISTS `{self._repo._TABLE_NAME}`")
        return


    def _get_data(self) -> list[GuildMemberHistory]:
        fixtures = FixturesApi()
        raw_test_data = [
                entity
                for datum in fixtures.get_guilds()[:10]
                for entity in self._adapter.Guild.to_guild_member_history(datum)
        ]
        raw_test_data = raw_test_data[:10]  # Get 10
        self.assertEquals(10, len(raw_test_data))

        testDatetime: datetime = datetime.fromtimestamp(1709181095)
        testData: list[GuildMemberHistory] = []
        for i, e in enumerate(raw_test_data):  # Modify the e id
            as_dict = self._repo._adapt(e)
            as_dict["uuid"] = UUID(int=i).bytes
            as_dict["datetime"] = testDatetime
            testData.append(e.__class__(**as_dict))
        return testData
