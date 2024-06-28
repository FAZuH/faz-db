# pyright: reportPrivateUsage=none
from datetime import datetime
from uuid import UUID

from tests.fixtures_api import FixturesApi
from fazdb.db.fazdb.model import GuildMemberHistory
from fazdb.db.fazdb.repository import GuildMemberHistoryRepository

from ._base_repository_testcase import BaseRepositoryTestCase


class TestGuildMemberHistoryRepository(BaseRepositoryTestCase[GuildMemberHistory]):

    def __init__(self, methodName: str) -> None:
        super().__init__(GuildMemberHistoryRepository, methodName)

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
        toTest1: list[GuildMemberHistory] = []
        testDatetime1 = datetime.fromtimestamp(1709181095)
        testUuid1 = UUID(int=69).bytes
        for e in self._testData:
            as_dict = self._repo._model_to_dict(e)
            as_dict["uuid"] = testUuid1
            as_dict["datetime"] = testDatetime1
            as_dict.pop("unique_id")  # type: ignore
            toTest1.append(e.__class__(**as_dict))  # type: ignore

        # ACT
        n = await self._repo.insert(toTest1)

        # ASSERT
        # NOTE: Assert unique constraints of character_uuid
        # self.assertEqual(1, n)  # TODO:

    async def asyncTearDown(self) -> None:
        await self._repo._db.execute(f"DROP TABLE IF EXISTS `{self._repo.table_name}`")
        return

    def _get_data(self) -> list[GuildMemberHistory]:
        fixtures = FixturesApi()
        raw_test_data = [
                entity
                for datum in fixtures.get_guilds()[:10]
                for entity in self._adapter.Guild.to_guild_member_history(datum)
        ]
        raw_test_data = raw_test_data[:10]  # Get 10
        self.assertEqual(10, len(raw_test_data))

        testDatetime: datetime = datetime.fromtimestamp(1709181095)
        testData: list[GuildMemberHistory] = []
        for i, e in enumerate(raw_test_data):  # Modify the e id
            as_dict = self._repo._model_to_dict(e)
            as_dict["uuid"] = UUID(int=i).bytes
            as_dict["datetime"] = testDatetime
            as_dict.pop("unique_id")  # type: ignore
            testData.append(e.__class__(**as_dict))  # type: ignore
        return testData
