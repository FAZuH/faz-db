# pyright: reportPrivateUsage=none
from copy import deepcopy
from datetime import datetime
from uuid import UUID

from tests.fixtures_api import FixturesApi
from fazdb.api.wynn.model.field import HeaderDateField, UsernameOrUuidField
from fazdb.db.fazdb.model import PlayerActivityHistory
from fazdb.db.fazdb.repository import PlayerActivityHistoryRepository

from ._base_repository_testcase import BaseRepositoryTestCase


class TestPlayerActivityHistoryRepository(BaseRepositoryTestCase):

    def __init__(self, methodName: str) -> None:
        super().__init__(PlayerActivityHistoryRepository, methodName)

    # override
    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()
        test_data = self.__get_data()
        self._testData1 = test_data[0]
        self._testData2 = test_data[1]

    async def test_create_table(self) -> None:
        # ACT
        await self._repo.create_table()

        # ASSERT
        await self.assert_table_exists()

    async def test_insert(self) -> None:
        # ACT
        n = await self._repo.insert(self._testData1)

        # ASSERT
        # NOTE: Assert if new players are inserted properly
        self.assertEqual(10, n)

        # ACT
        n = await self._repo.insert(self._testData2)

        # ASSERT
        # NOTE: Assert if new players are inserted properly
        # self.assertEqual(15, len(await self._repo.find_all()))  # TODO:

    async def asyncTearDown(self) -> None:
        await self._repo._db.execute(f"DROP TABLE IF EXISTS `{self._repo.table_name}`")
        return

    def _get_data(self):
        return None

    def __get_data(self) -> tuple[list[PlayerActivityHistory], list[PlayerActivityHistory]]:
        testDatetime1 = datetime.fromtimestamp(1_709_181_095)
        testDatetime2 = datetime.fromtimestamp(1_709_181_195)  # + 100
        testDatetime3 = datetime.fromtimestamp(1_709_180_095)  # - 1000
        testDatetime4 = datetime.fromtimestamp(1_709_180_095)  # - 1000
        testOnlinePlayers1 = {
                UsernameOrUuidField(str(UUID(int=i + 1))): ''
                for i in range(10)
        }
        testOnlinePlayers2 = {
                UsernameOrUuidField(str(UUID(int=i + 1))): ''
                for i in range(5, 15)
        }

        fixtures = FixturesApi()
        resp = fixtures.get_online_uuids()

        resp1  = deepcopy(resp)
        resp2 = deepcopy(resp)

        resp1.body._players = testOnlinePlayers1
        resp2.body._players = testOnlinePlayers2
        resp1.headers._expires = HeaderDateField(testDatetime1.isoformat())
        resp1.headers._expires = HeaderDateField(testDatetime2.isoformat())

        raw_test_data1 = list(self._adapter.OnlinePlayers.to_player_activity_history(
                resp1, {uuid.username_or_uuid: testDatetime3 for uuid in resp1.body.players}  # type: ignore
        ))
        raw_test_data2 = list(self._adapter.OnlinePlayers.to_player_activity_history(
                resp2, {uuid.username_or_uuid: testDatetime4 for uuid in resp2.body.players}  # type: ignore
        ))

        self.assertEqual(10, len(raw_test_data1))
        self.assertEqual(10, len(raw_test_data2))
        return raw_test_data1, raw_test_data2
