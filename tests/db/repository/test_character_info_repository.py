# pyright: reportPrivateUsage=none
import unittest
from uuid import UUID

from loguru import logger

from kans import config
from kans.db import KansDatabase
from kans.db.kans.model import CharacterInfo, CharacterInfoId
from kans.util import ApiResponseAdapter
from tests.fixtures_api import FixturesApi


class TestCharacterInfoRepository(unittest.IsolatedAsyncioTestCase):
    # self.repo to access repo
    # self.test_data to access test data

    async def asyncSetUp(self) -> None:
        self._adapter = ApiResponseAdapter()
        self._db = KansDatabase(config, logger)
        self._repo = self._db.character_info_repository

        self._repo._TABLE_NAME = "test_character_info"
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
        toTest1: list[CharacterInfo] = []
        testUuid1 = UUID(int=69).bytes
        for e in self._testData:
            as_dict = self._repo._adapt(e)
            as_dict["character_uuid"] = testUuid1
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
        exists = [await self._repo.exists(CharacterInfoId(e.character_uuid)) for e in self._testData]

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
        found: list[CharacterInfo] = []
        for e in self._testData:
            # Find the inserted e
            res = await self._repo.find_one(CharacterInfoId(e.character_uuid))
            if res is not None:
                found.append(res)

        # ASSERT
        found_uuids = {e.character_uuid.uuid for e in found}
        test_uuids = {e.character_uuid.uuid for e in self._testData}
        # NOTE: Assert if the number of found entities is the same as the inserted entities
        self.assertEquals(len(self._testData), len(found))
        # NOTE: Assert if the found entities are the same as the inserted entities
        self.assertSetEqual(found_uuids, test_uuids)

    async def test_find_all(self) -> None:
        # PREPARE
        await self._repo.insert(self._testData)

        # ACT
        found = await self._repo.find_all()

        # ASSERT
        found_uuids = {e.character_uuid.uuid for e in found}
        test_uuids = {e.character_uuid.uuid for e in self._testData}
        # NOTE: Assert if the number of found entities is the same as the inserted entities
        self.assertEquals(len(self._testData), len(found))
        # NOTE: Assert if the found entities are the same as the inserted entities
        self.assertSetEqual(found_uuids, test_uuids)

    async def test_update(self) -> None:
        # PREPARE
        testType2 = "MAGE"
        for e in self._testData:
            e._type = testType2
        await self._repo.insert(self._testData)
        testType1 = "WARRIOR"
        for e in self._testData:
            e._type = testType1

        # ACT
        n = await self._repo.update(self._testData)

        # ASSERT
        # NOTE: Assert if the number of updated entities is correct
        self.assertEquals(len(self._testData), n)
        for e in (await self._repo.find_all()):
            # NOTE: Assert if the updated e is the same as the updated values
            self.assertEquals(testType1, e.type)

    async def test_delete(self) -> None:
        # PREPARE
        await self._repo.insert(self._testData)

        # ACT
        n = await self._repo.delete(CharacterInfoId(self._testData[0].character_uuid))

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


    def _get_data(self) -> list[CharacterInfo]:
        fixtures = FixturesApi()
        raw_test_data = [
                e
                for datum in fixtures.get_players()[:10]
                for e in self._adapter.Player.to_character_info(datum)
        ]
        raw_test_data = raw_test_data[:10]  # Get 10
        self.assertEquals(10, len(raw_test_data))

        testData: list[CharacterInfo] = []
        for i, e in enumerate(raw_test_data):  # Modify the e id
            as_dict = self._repo._adapt(e)
            as_dict["character_uuid"] = UUID(int=i).bytes
            testData.append(e.__class__(**as_dict))
        return testData
