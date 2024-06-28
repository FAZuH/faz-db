# pyright: reportPrivateUsage=none
from datetime import datetime

from tests.fixtures_api import FixturesApi
from fazdb.db.fazdb.model import GuildHistory
from fazdb.db.fazdb.repository import GuildHistoryRepository

from ._base_repository_testcase import BaseRepositoryTestCase


class TestGuildHistoryRepository(BaseRepositoryTestCase[GuildHistory]):

    def __init__(self, methodName: str) -> None:
        super().__init__(GuildHistoryRepository, methodName)

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
        toTest1: list[GuildHistory] = self._testData[1:]
        as_dict = self._repo._model_to_dict(self._testData[0])
        as_dict["level"] += 1
        as_dict.pop("unique_id")  # type: ignore
        toTest1.append(GuildHistory(**as_dict))  # type: ignore

        # ACT
        n = await self._repo.insert(toTest1)

        # ASSERT
        # NOTE: Assert unique constraints of character_uuid
        self.assertEqual(1, n)

    async def asyncTearDown(self) -> None:
        await self._repo._db.execute(f"DROP TABLE IF EXISTS `{self._repo.table_name}`")
        return

    def _get_data(self) -> list[GuildHistory]:
        fixtures = FixturesApi()
        raw_test_data = [
                self._adapter.Guild.to_guild_history(datum)
                for datum in fixtures.get_guilds()[:10]
        ]
        raw_test_data = raw_test_data[:10]  # Get 10
        self.assertEqual(10, len(raw_test_data))

        testDatetime = datetime.fromtimestamp(1709181095)
        testData: list[GuildHistory] = []
        for i, e in enumerate(raw_test_data):  # Modify the e id
            as_dict = self._repo._model_to_dict(e)
            as_dict["name"] = str(i)
            as_dict["datetime"] = testDatetime
            as_dict.pop("unique_id")  # type: ignore
            testData.append(e.__class__(**as_dict))  # type: ignore
        return testData
