# pyright: reportPrivateUsage=none
import unittest
from datetime import datetime
from uuid import UUID

from wynndb.config import Config
from wynndb.db import KansDatabase
from wynndb.db.wynndb.model import PlayerHistory
from wynndb.logger.kans_logger import KansLogger
from wynndb.util import ApiResponseAdapter
from tests.fixtures_api import FixturesApi


class TestPlayerHistoryRepository(unittest.IsolatedAsyncioTestCase):
    # self.repo to access repo
    # self.test_data to access test data

    async def asyncSetUp(self) -> None:
        self._adapter = ApiResponseAdapter()
        config = Config()
        self._db = KansDatabase(config, KansLogger(config))
        self._repo = self._db.player_history_repository

        self._repo._TABLE_NAME = "test_player_history"
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
        toTest1: list[PlayerHistory] = []
        testDatetime1 = datetime.fromtimestamp(1709181095)
        testUuid1 = UUID(int=69).bytes
        for e in self._testData:
            as_dict = self._repo._adapt(e)
            as_dict["uuid"] = testUuid1
            as_dict["datetime"] = testDatetime1
            as_dict.pop("unique_id")  # type: ignore
            toTest1.append(e.__class__(**as_dict))  # type: ignore

        # ACT
        n = await self._repo.insert(toTest1)

        # ASSERT
        # NOTE: Assert unique constraints of uuid and datetime
        # self.assertEquals(1, n)  # TODO:

    async def asyncTearDown(self) -> None:
        await self._repo._db.execute(f"DROP TABLE IF EXISTS `{self._repo._TABLE_NAME}`")
        return

    def _get_data(self) -> list[PlayerHistory]:
        fixtures = FixturesApi()
        raw_test_data = [
                self._adapter.Player.to_player_history(datum)
                for datum in fixtures.get_players()[:10]
        ]
        raw_test_data = raw_test_data[:10]  # Get 10
        self.assertEquals(10, len(raw_test_data))

        testDatetime = datetime.fromtimestamp(1709181095)
        testData: list[PlayerHistory] = []
        for i, e in enumerate(raw_test_data):  # Modify the e id
            as_dict = self._repo._adapt(e)
            as_dict["uuid"] = UUID(int=i).bytes
            as_dict["datetime"] = testDatetime
            as_dict.pop("unique_id")  # type: ignore
            testData.append(e.__class__(**as_dict))  # type: ignore
        return testData
