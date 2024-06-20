# pyright: reportPrivateUsage=none
from uuid import UUID

from tests.fixtures_api import FixturesApi
from wynndb.db.wynndb.model import OnlinePlayers
from wynndb.db.wynndb.repository import OnlinePlayersRepository

from ._base_repository_testcase import BaseRepositoryTestCase


class TestOnlinePlayersRepository(BaseRepositoryTestCase[OnlinePlayers]):

    def __init__(self, methodName: str) -> None:
        super().__init__(OnlinePlayersRepository, methodName)

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
        toTest1: list[OnlinePlayers] = []
        for i, e in enumerate(self._testData):
            as_dict = self._repo._model_to_dict(e)
            as_dict["uuid"] = UUID(int=69 + i).bytes
            toTest1.append(e.__class__(**as_dict))

        # ACT
        n = await self._repo.insert(toTest1)

        # ASSERT
        # NOTE: Assert unique constraints.
        # self.assertEqual(len(toTest1), (await self._repo.count()))  # TODO:

    async def asyncTearDown(self) -> None:
        await self._repo._db.execute(f"DROP TABLE IF EXISTS `{self._repo.table_name}`")
        return

    def _get_data(self) -> list[OnlinePlayers]:
        fixtures = FixturesApi()
        raw_test_data = list(self._adapter.OnlinePlayers.to_online_players(fixtures.get_online_uuids()))
        raw_test_data = raw_test_data[:10]  # Get 10
        self.assertEqual(10, len(raw_test_data))

        testData: list[OnlinePlayers] = []
        for i, e in enumerate(raw_test_data):  # Ensure unique ids
            as_dict = self._repo._model_to_dict(e)
            as_dict["uuid"] = UUID(int=i).bytes
            testData.append(e.__class__(**as_dict))
        return testData
