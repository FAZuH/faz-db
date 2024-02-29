# pyright: reportPrivateUsage=none
import unittest
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from loguru import logger

from kans import config
from kans.db import KansDatabase
from kans.db.model import CharacterHistory, CharacterHistoryId
from kans.util import ApiResponseAdapter
from tests.fixtures_api import FixturesApi


class TestCharacterHistoryRepository(unittest.IsolatedAsyncioTestCase):
    # self.repo to access repo
    # self.test_data to access test data

    async def asyncSetUp(self) -> None:
        self._adapter = ApiResponseAdapter()
        self._db = KansDatabase(config, logger)
        self._repo = self._db.character_history_repository
        self._repo._TABLE_NAME = "test_character_history"
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
            res = await self._repo.exists(CharacterHistoryId(e.character_uuid, e.datetime))
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
        found: list[CharacterHistory] = []
        for e in self._test_data:
            # Find the inserted e
            res = await self._repo.find_one(CharacterHistoryId(e.character_uuid, e.datetime))
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

    async def test_update(self) -> None:
        # PREPARE
        decimal = Decimal("100")
        await self._repo.insert(self._test_data)
        for e in self._test_data:
            e._alchemism = decimal

        # ACT
        n = await self._repo.update(self._test_data)

        # PREPARE
        found = await self._repo.find_all()

        # ASSERT
        # NOTE: Assert if the number of updated entities is correct
        self.assertEquals(len(self._test_data), n)
        for e in found:
            # NOTE: Assert if the updated e is the same as the updated values
            self.assertEquals(decimal, e.alchemism)

    async def test_delete(self) -> None:
        # PREPARE
        await self._repo.insert(self._test_data)

        # ACT
        n = await self._repo.delete(CharacterHistoryId(self._test_data[0].character_uuid, self._test_data[0].datetime))

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

    def _get_data(self) -> list[CharacterHistory]:
        fixtures = FixturesApi()
        raw_test_data = [
                e
                for datum in fixtures.get_players()[:10]
                for e in self._adapter.Player.to_character_history(datum)
        ]
        raw_test_data = raw_test_data[:10]  # Get 10
        self.assertEquals(10, len(raw_test_data))

        now = datetime.fromtimestamp(1709181095)
        test_data: list[CharacterHistory] = []
        for i, e in enumerate(raw_test_data):  # Modify the e id
            as_dict = self._repo._adapt(e)
            as_dict["character_uuid"] = UUID(int=i).bytes
            as_dict["datetime"] = now
            test_data.append(e.__class__(**as_dict))
        return test_data
