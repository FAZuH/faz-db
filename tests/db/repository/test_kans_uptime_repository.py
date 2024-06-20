# pyright: reportPrivateUsage=none
from datetime import datetime

from wynndb.db.wynndb.model import WynnDbUptime
from wynndb.db.wynndb.repository import WynnDbUptimeRepository

from ._base_repository_testcase import BaseRepositoryTestCase


class TestWynnDbUptimeRepository(BaseRepositoryTestCase[WynnDbUptime]):

    def __init__(self, methodName: str) -> None:
        super().__init__(WynnDbUptimeRepository, methodName)

    async def test_create_table(self) -> None:
        # ACT
        await self._repo.create_table()

        # ASSERT
        await self.assert_table_exists()

    async def test_insert(self) -> None:
        # ACT
        await self._repo.insert(self._testData)

        # ASSERT
        # NOTE: Assert if the number of inserted entities is correct
        res = await self._repo._db.fetch(f"SELECT * FROM {self._repo.table_name}")
        self.assertEqual(2, len(res))

    async def asyncTearDown(self) -> None:
        await self._repo._db.execute(f"DROP TABLE IF EXISTS `{self._repo.table_name}`")
        return

    def _get_data(self) -> list[WynnDbUptime]:
        testTimestamp1 = 1709181095
        testData: list[WynnDbUptime] = [
                WynnDbUptime(
                        start_time=datetime.fromtimestamp(testTimestamp1),
                        stop_time=datetime.fromtimestamp(testTimestamp1 + i)
                )
                for i in range(5)
        ]
        testData.extend(
                WynnDbUptime(
                        start_time=datetime.fromtimestamp(testTimestamp1 + 10),
                        stop_time=datetime.fromtimestamp(testTimestamp1 + i)
                )
                for i in range(5)
        )
        return testData
