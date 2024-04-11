# pyright: reportPrivateUsage=none
import unittest

from wynndb.config import Config
from wynndb.db import KansDatabase
from wynndb.db.wynndb.model import GuildInfo
from wynndb.logger.kans_logger import KansLogger
from wynndb.util import ApiResponseAdapter
from tests.fixtures_api import FixturesApi


class TestGuildInfoRepository(unittest.IsolatedAsyncioTestCase):
    # self.repo to access repo
    # self.test_data to access test data

    async def asyncSetUp(self) -> None:
        self._adapter = ApiResponseAdapter()
        config = Config()
        self._db = KansDatabase(config, KansLogger(config))
        self._repo = self._db.guild_info_repository

        self._repo._TABLE_NAME = "test_guild_info"
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
        toTest1: list[GuildInfo] = []
        testName = "test"
        for e in self._testData:
            as_dict = self._repo._adapt(e)
            as_dict["name"] = testName
            toTest1.append(e.__class__(**as_dict))

        # ACT
        n = await self._repo.insert(toTest1)

        # ASSERT
        # NOTE: Assert unique constraints of character_uuid
        self.assertEquals(1, n)

    async def asyncTearDown(self) -> None:
        await self._repo._db.execute(f"DROP TABLE IF EXISTS `{self._repo._TABLE_NAME}`")
        return

    def _get_data(self) -> list[GuildInfo]:
        fixtures = FixturesApi()
        raw_test_data = [
                self._adapter.Guild.to_guild_info(datum)
                for datum in fixtures.get_guilds()[:10]
        ]
        raw_test_data = raw_test_data[:10]  # Get 10
        self.assertEquals(10, len(raw_test_data))

        testData: list[GuildInfo] = []
        for i, e in enumerate(raw_test_data):  # Modify the e id
            as_dict = self._repo._adapt(e)
            as_dict["name"] = str(i)
            testData.append(e.__class__(**as_dict))
        return testData
