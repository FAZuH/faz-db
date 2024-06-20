# pyright: reportPrivateUsage=none
from unittest import IsolatedAsyncioTestCase
from datetime import datetime
from uuid import UUID

from wynndb.config import Config
from wynndb.db import WynnDbDatabase
from wynndb.db.wynndb.model import CharacterHistory
from wynndb.logger.wynndb_logger import WynnDbLogger
from wynndb.util import ApiResponseAdapter
from tests.fixtures_api import FixturesApi


class TestCharacterHistoryRepository(IsolatedAsyncioTestCase):
    # self.repo to access repo
    # self.test_data to access test data

    async def asyncSetUp(self) -> None:
        Config.load_config()
        self._adapter = ApiResponseAdapter()
        self._db = WynnDbDatabase(WynnDbLogger())
        self._repo = self._db.character_history_repository

        self._repo._TABLE_NAME = "test_character_history"
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
        n = await self._repo.insert(self._testData)

        # ASSERT
        # NOTE: Assert if the number of inserted entities is correct
        self.assertEqual(10, n)

        # PREPARE
        toTest1: list[CharacterHistory] = self._testData[1:]
        as_dict = self._repo._adapt(self._testData[0])
        as_dict["level"] += 1
        as_dict.pop("unique_id")  # type: ignore
        toTest1.append(CharacterHistory(**as_dict))  # type: ignore

        # ACT
        n = await self._repo.insert(toTest1)

        # ASSERT
        # NOTE: Assert unique constraints of character_uuid and datetime
        self.assertEqual(1, n)

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
        self.assertEqual(10, len(raw_test_data))

        testDatetime = datetime.fromtimestamp(1709181095)
        testData: list[CharacterHistory] = []
        for i, e in enumerate(raw_test_data):  # Modify the e id
            as_dict = self._repo._adapt(e)
            as_dict["character_uuid"] = UUID(int=i).bytes
            as_dict["datetime"] = testDatetime
            as_dict.pop("unique_id")  # type: ignore
            testData.append(e.__class__(**as_dict))  # type: ignore
        return testData
