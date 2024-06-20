# pyright: reportPrivateUsage=none
from tests.fixtures_api import FixturesApi
from wynndb.db.wynndb.model import GuildInfo
from wynndb.db.wynndb.repository import GuildInfoRepository

from ._base_repository_testcase import BaseRepositoryTestCase


class TestGuildInfoRepository(BaseRepositoryTestCase[GuildInfo]):

    def __init__(self, methodName: str) -> None:
        super().__init__(GuildInfoRepository, methodName)

    async def test_create_table(self) -> None:
        # ACT
        await self._repo.create_table()

        # ASSERT
        await self.assert_table_exists()

    async def test_insert(self) -> None:
        # ACT
        n = await self._repo.insert(self._testData)

        # ASSERT
        # NOTE: Assert if the number of inserted entities is correct
        self.assertEqual(10, n)

        # PREPARE
        toTest1: list[GuildInfo] = []
        testName = "test"
        for e in self._testData:
            as_dict = self._repo._model_to_dict(e)
            as_dict["name"] = testName
            toTest1.append(e.__class__(**as_dict))

        # ACT
        n = await self._repo.insert(toTest1)

        # ASSERT
        # NOTE: Assert unique constraints of character_uuid
        self.assertEqual(1, n)

    async def asyncTearDown(self) -> None:
        await self._repo._db.execute(f"DROP TABLE IF EXISTS `{self._repo.table_name}`")
        return

    def _get_data(self) -> list[GuildInfo]:
        fixtures = FixturesApi()
        raw_test_data = [
                self._adapter.Guild.to_guild_info(datum)
                for datum in fixtures.get_guilds()[:10]
        ]
        raw_test_data = raw_test_data[:10]  # Get 10
        self.assertEqual(10, len(raw_test_data))

        testData: list[GuildInfo] = []
        for i, e in enumerate(raw_test_data):  # Modify the e id
            as_dict = self._repo._model_to_dict(e)
            as_dict["name"] = str(i)
            testData.append(e.__class__(**as_dict))
        return testData
