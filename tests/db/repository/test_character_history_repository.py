# pyright: reportPrivateUsage=none
from datetime import datetime
from uuid import UUID

from tests.fixtures_api import FixturesApi
from wynndb.db.wynndb.model import CharacterHistory
from wynndb.db.wynndb.repository import CharacterHistoryRepository

from ._base_repository_testcase import BaseRepositoryTestCase


class TestCharacterHistoryRepository(BaseRepositoryTestCase[CharacterHistory]):

    def __init__(self, methodName: str) -> None:
        super().__init__(CharacterHistoryRepository, methodName)

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
        toTest1: list[CharacterHistory] = self._testData[1:]
        as_dict = self._repo._model_to_dict(self._testData[0])
        as_dict["level"] += 1
        as_dict.pop("unique_id")  # type: ignore
        toTest1.append(CharacterHistory(**as_dict))  # type: ignore

        # ACT
        n = await self._repo.insert(toTest1)

        # ASSERT
        # NOTE: Assert unique constraints of character_uuid and datetime
        self.assertEqual(1, n)

    def _get_data(self) -> list[CharacterHistory]:
        fixtures = FixturesApi()
        raw_test_data = [
                e
                for datum in fixtures.get_players()[:10]
                for e in self._adapter.Player.to_character_history(datum)
        ]
        raw_test_data = raw_test_data[:10]  # Get 10
        self.assertEqual(10, len(raw_test_data))

        testDatetime = datetime.fromtimestamp(1709181095)
        testData: list[CharacterHistory] = []
        for i, e in enumerate(raw_test_data):  # Modify the e id
            as_dict = self._repo._model_to_dict(e)
            as_dict["character_uuid"] = UUID(int=i).bytes
            as_dict["datetime"] = testDatetime
            as_dict.pop("unique_id")  # type: ignore
            testData.append(e.__class__(**as_dict))  # type: ignore
        return testData
