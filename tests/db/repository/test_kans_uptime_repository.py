# pyright: reportPrivateUsage=none
from datetime import datetime

from fazdb.db.fazdb.model import FazDbUptime
from fazdb.db.fazdb.repository import FazDbUptimeRepository

from ._base_repository_testcase import BaseRepositoryTestCase


class TestFazDbUptimeRepository(BaseRepositoryTestCase[FazDbUptime]):

    def __init__(self, methodName: str) -> None:
        super().__init__(FazDbUptimeRepository, methodName)

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

    def _get_data(self) -> list[FazDbUptime]:
        testTimestamp1 = 1709181095
        testData: list[FazDbUptime] = [
                FazDbUptime(
                        start_time=datetime.fromtimestamp(testTimestamp1),
                        stop_time=datetime.fromtimestamp(testTimestamp1 + i)
                )
                for i in range(5)
        ]
        testData.extend(
                FazDbUptime(
                        start_time=datetime.fromtimestamp(testTimestamp1 + 10),
                        stop_time=datetime.fromtimestamp(testTimestamp1 + i)
                )
                for i in range(5)
        )
        return testData
