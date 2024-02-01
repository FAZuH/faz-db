import unittest

from tests.mock_wynnapi import MockWynnApi
# from vindicator import (
#     config,
#     DatabaseBase,
#     PlayerResponse,
#     PlayersResponse,
#     GuildResponse,
#     WynnDataRepository
# )
from vindicator import *


class TestWynnDbRepository(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.mockwynnapi = MockWynnApi()
        self.wynnapi = self.mockwynnapi.wynnapi
        # await self.wynnapi.start()

        self.toTest_guildStats = self.mockwynnapi.onlineGuildStats
        self.toTest_onlineUuids = self.mockwynnapi.onlineUuids
        self.toTest_playerStats = self.mockwynnapi.onlinePlayerStats

        self.wynndb: DatabaseQuery = DatabaseQuery(
            config['WYNNDATA_DB_USER'], config['WYNNDATA_DB_PASSWORD'], config['WYNNDATA_DB_DBNAME'], 2
        )
        self.wynnrepo: WynnDataRepository = WynnDataRepository(self.wynndb)

    # @vcr(use_cassette)
    async def test_character_history_repo(self) -> None:
        if self.toTest_guildStats is None:
            self.assertTrue(False)
            return
        self.wynnrepo.character_history_repository._TABLE_NAME = "temp_character_history"
        try:
            await self.wynnrepo.character_history_repository.create_table()
            for playerStat in self.toTest_playerStats:
                player_hists = CharacterHistory.from_response(playerStat)
                for player_hist in player_hists:
                    b = await self.wynnrepo.character_history_repository.insert(player_hist)
                    self.assertTrue(b)
        except Exception:
            raise
        finally:
            await self.wynndb.execute("DROP TABLE temp_character_history")
        return


    async def asyncTearDown(self) -> None:
        # await self.wynnapi.close()
        return
