# pyright: reportPrivateUsage=none
import unittest
from uuid import UUID

from loguru import logger

from kans import config
from kans.db import KansDatabase
from kans.db.model import CharacterInfo, CharacterInfoId
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

        self._test_data = self._get_data()


    async def test_create_table(self) -> None:
        # ACT
        await self._repo.create_table()

        # ASSERT
        # NOTE: Assert if the table exists
        res = await self._repo._db.fetch(f"SHOW TABLES LIKE '{self._repo._TABLE_NAME}'")
        self.assertEquals(self._repo.table_name, next(iter(res[0].values())))

    async def test_insert(self) -> None:
        # ACT
        n = await self._repo.insert(self._test_data)

        # ASSERT
        # NOTE: Assert if the number of inserted entities is correct
        self.assertEquals(10, n)

    async def test_exists(self) -> None:
        # PREPARE
        await self._repo.insert(self._test_data)

        # ACT
        exists = []
        for e in self._test_data:
            # Check if the e exists
            res = await self._repo.exists(CharacterInfoId(e.character_uuid))
            exists.append(res)

        # ASSERT
        # NOTE: Assert if the number of existing entities is the same as the inserted entities
        self.assertEquals(len(self._test_data), len(exists))
        # NOTE: Assert if all the entities exist
        self.assertTrue(all(exists))

    async def test_count(self) -> None:
        # PREPARE
        await self._repo.insert(self._test_data)

        # ACT
        count = await self._repo.count()

        # ASSERT
        # NOTE: Assert if the number of inserted entities is the same as the count
        self.assertEquals(len(self._test_data), count)

    async def test_find_one(self) -> None:
        # PREPARE
        await self._repo.insert(self._test_data)

        # ACT
        found: list[CharacterInfo] = []
        for e in self._test_data:
            # Find the inserted e
            res = await self._repo.find_one(CharacterInfoId(e.character_uuid))
            if res is not None:
                found.append(res)

        # ASSERT
        found_uuids = {e.character_uuid.uuid for e in found}
        test_uuids = {e.character_uuid.uuid for e in self._test_data}
        # NOTE: Assert if the number of found entities is the same as the inserted entities
        self.assertEquals(len(self._test_data), len(found))
        # NOTE: Assert if the found entities are the same as the inserted entities
        self.assertSetEqual(found_uuids, test_uuids)

    async def test_find_all(self) -> None:
        # PREPARE
        await self._repo.insert(self._test_data)

        # ACT
        found = await self._repo.find_all()

        # ASSERT
        found_uuids = {e.character_uuid.uuid for e in found}
        test_uuids = {e.character_uuid.uuid for e in self._test_data}
        # NOTE: Assert if the number of found entities is the same as the inserted entities
        self.assertEquals(len(self._test_data), len(found))
        # NOTE: Assert if the found entities are the same as the inserted entities
        self.assertSetEqual(found_uuids, test_uuids)

    @unittest.skip("Update method is not implemented in CharacterInfoRepository")
    async def test_update(self) -> None:
        pass

    async def test_delete(self) -> None:
        # PREPARE
        await self._repo.insert(self._test_data)

        # ACT
        n = await self._repo.delete(CharacterInfoId(self._test_data[0].character_uuid))

        # PREPARE
        found = await self._repo.find_all()

        # ASSERT
        # NOTE: Assert if the number of deleted entities is correct
        self.assertEquals(1, n)
        # NOTE: Assert if the number of found entities is correct
        self.assertEquals(len(self._test_data) - 1, len(found))


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

        test_data: list[CharacterInfo] = []
        for i, e in enumerate(raw_test_data):  # Modify the e id
            as_dict = self._repo._adapt(e)
            as_dict["character_uuid"] = UUID(int=i).bytes
            as_dict["type"] = "WARRIOR"
            test_data.append(e.__class__(**as_dict))
        return test_data
