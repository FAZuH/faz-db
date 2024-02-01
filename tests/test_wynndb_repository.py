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

        self.wynndb: DatabaseQuery = DatabaseQuery(config['WYNNDATA_DB_USER'], config['WYNNDATA_DB_PASSWORD'], config['WYNNDATA_DB_DATABASE'], 2)
        self.wynnrepo: WynnDataRepository = WynnDataRepository(self.wynndb)

    # # @vcr(use_cassette)
    # async def test_guild_history(self) -> None:
    #     if self.toTest_guildStats is None:
    #         self.assertTrue(False)
    #         return

    #     for guildStat in self.toTest_guildStats:
    #         guild_hist = GuildHistory.from_response(guildStat)
    #         guild_hist.
    #         await self.wynnrepo.guild_history_repository.insert(guild_hist)
    #     pass

    async def asyncTearDown(self) -> None:
        # await self.wynnapi.close()
        return
