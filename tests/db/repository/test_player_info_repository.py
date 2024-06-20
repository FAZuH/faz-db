# pyright: reportPrivateUsage=none
from uuid import UUID

from tests.fixtures_api import FixturesApi
from wynndb.db.wynndb.model import PlayerInfo
from wynndb.db.wynndb.repository import PlayerInfoRepository

from ._base_repository_testcase import BaseRepositoryTestCase


class TestPlayerInfoRepository(BaseRepositoryTestCase[PlayerInfo]):

    def __init__(self, methodName: str) -> None:
        super().__init__(PlayerInfoRepository, methodName)

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

    async def asyncTearDown(self) -> None:
        await self._repo._db.execute(f"DROP TABLE IF EXISTS `{self._repo.table_name}`")
        return


    def _get_data(self) -> list[PlayerInfo]:
        fixtures = FixturesApi()
        raw_test_data = [
                self._adapter.Player.to_player_info(datum)
                for datum in fixtures.get_players()[:10]
        ]
        raw_test_data = raw_test_data[:10]  # Get 10
        self.assertEqual(10, len(raw_test_data))

        testData: list[PlayerInfo] = []
        for i, e in enumerate(raw_test_data):  # Modify the e id
            as_dict = self._repo._model_to_dict(e)
            as_dict["uuid"] = UUID(int=i).bytes
            testData.append(e.__class__(**as_dict))
        return testData
