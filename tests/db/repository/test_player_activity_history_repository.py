# pyright: reportPrivateUsage=none
from copy import deepcopy
from datetime import datetime
import unittest
from uuid import UUID

from wynndb.config import Config
from wynndb.api.wynn.model.field import HeaderDateField
from wynndb.api.wynn.model.field import UsernameOrUuidField
from wynndb.db import WynnDbDatabase
from wynndb.db.wynndb.model import PlayerActivityHistory
from wynndb.logger.wynndb_logger import WynnDbLogger
from wynndb.util import ApiResponseAdapter
from tests.fixtures_api import FixturesApi


class TestPlayerActivityHistoryRepository(unittest.IsolatedAsyncioTestCase):
    # self.repo to access repo
    # self.test_data to access test data

    async def asyncSetUp(self) -> None:
        Config.load_config()
        self._adapter = ApiResponseAdapter()
        self._db = WynnDbDatabase(WynnDbLogger())
        self._repo = self._db.player_activity_history_repository

        self._repo._TABLE_NAME = "test_player_activity_history"
        await self._repo.create_table()

        testData = self._get_data()
        self._testData1 = testData[0]
        self._testData2 = testData[1]

    async def test_create_table(self) -> None:
        # ACT
        await self._repo.create_table()

        # ASSERT
        # NOTE: Assert if the table exists
        res = await self._repo._db.fetch(f"SHOW TABLES LIKE '{self._repo._TABLE_NAME}'")
        self.assertEqual(self._repo.table_name, next(iter(res[0].values())))

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
        await self._repo._db.execute(f"DROP TABLE IF EXISTS `{self._repo._TABLE_NAME}`")
        return

    def _get_data(self) -> tuple[list[PlayerActivityHistory], list[PlayerActivityHistory]]:
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
