from time import perf_counter
import unittest

from tests.mock_wynnapi import MockWynnApi
from src import (
    logger,
    CharacterInfo,
    GuildHistory,
    GuildInfo,
    GuildMemberHistory,
    OnlinePlayers,
    # PlayerActivityHistory,
    PlayerHistory,
    PlayerInfo,
    WynnDataRepository
)
from src import *


class TestWynnDbRepository(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.mockwynnapi = MockWynnApi()
        self.wynnapi = self.mockwynnapi.wynnapi
        # await self.wynnapi.start()

        self.mock_guildstats = self.mockwynnapi.onlineguildstats
        self.mock_onlineuuids = self.mockwynnapi.onlineuuids
        self.mock_playerstats = self.mockwynnapi.onlineplayerstats

        self.wynnrepo: WynnDataRepository = WynnDataRepository()

    # @vcr(use_cassette)
    async def test_character_history_repo(self) -> None:
        if self.mock_playerstats is None:
            self.assertTrue(False)
            return
        self.wynnrepo.character_history_repository._TABLE_NAME = "temp_character_history"  # type: ignore
        try:
            await self.wynnrepo.character_history_repository.create_table()
            t1 = perf_counter()
            l = CharacterHistory.from_responses(self.mock_playerstats)
            affectedrows = await self.wynnrepo.character_history_repository.insert(l)
            t2 = perf_counter()
            logger.success(f"inserted {len(l)} rows in {t2 - t1} seconds")
            self.assertGreaterEqual(affectedrows, 0)
        except Exception:
            raise
        finally:
            await self.wynnrepo.wynndb.execute("DROP TABLE temp_character_history")

    async def test_character_info_repo(self) -> None:
        if self.mock_playerstats is None:
            self.assertTrue(False)
            return
        self.wynnrepo.character_info_repository._TABLE_NAME = "temp_character_info"  # type: ignore
        try:
            await self.wynnrepo.character_info_repository.create_table()
            t1 = perf_counter()
            l = CharacterInfo.from_responses(self.mock_playerstats)
            affectedrows = await self.wynnrepo.character_info_repository.insert(l)
            t2 = perf_counter()
            logger.success(f"inserted {len(l)} rows in {t2 - t1} seconds")
            self.assertGreaterEqual(affectedrows, 0)
        except Exception:
            raise
        finally:
            await self.wynnrepo.wynndb.execute("DROP TABLE temp_character_info")

    async def test_guild_history_repo(self) -> None:
        if self.mock_guildstats is None:
            self.assertTrue(False)
            return
        self.wynnrepo.guild_history_repository._TABLE_NAME = "temp_guild_history"  # type: ignore
        try:
            await self.wynnrepo.guild_history_repository.create_table()
            t1 = perf_counter()
            l = GuildHistory.from_responses(self.mock_guildstats)
            affectedrows = await self.wynnrepo.guild_history_repository.insert(l)
            t2 = perf_counter()
            logger.success(f"inserted {len(l)} rows in {t2 - t1} seconds")
            self.assertGreaterEqual(affectedrows, 0)
        except Exception:
            raise
        finally:
            await self.wynnrepo.wynndb.execute("DROP TABLE temp_guild_history")

    async def test_guild_info_repo(self) -> None:
        if self.mock_guildstats is None:
            self.assertTrue(False)
            return
        self.wynnrepo.guild_info_repository._TABLE_NAME = "temp_guild_info"  # type: ignore
        try:
            await self.wynnrepo.guild_info_repository.create_table()
            t1 = perf_counter()
            l = GuildInfo.from_responses(self.mock_guildstats)
            affectedrows = await self.wynnrepo.guild_info_repository.insert(l)
            t2 = perf_counter()
            logger.success(f"inserted {len(l)} rows in {t2 - t1} seconds")
            self.assertGreaterEqual(affectedrows, 0)
        except Exception:
            raise
        finally:
            await self.wynnrepo.wynndb.execute("DROP TABLE temp_guild_info")

    async def test_guild_member_history_repo(self) -> None:
        if self.mock_guildstats is None:
            self.assertTrue(False)
            return
        self.wynnrepo.guild_member_history_repository._TABLE_NAME = "temp_guild_member_history"  # type: ignore
        try:
            await self.wynnrepo.guild_member_history_repository.create_table()
            t1 = perf_counter()
            l = GuildMemberHistory.from_responses(self.mock_guildstats)
            affectedrows = await self.wynnrepo.guild_member_history_repository.insert(l)
            t2 = perf_counter()
            logger.success(f"inserted {len(l)} rows in {t2 - t1} seconds")
            self.assertGreaterEqual(affectedrows, 0)
        except Exception:
            raise
        finally:
            await self.wynnrepo.wynndb.execute("DROP TABLE temp_guild_member_history")

    async def test_online_players_repo(self) -> None:
        if self.mock_onlineuuids is None:
            self.assertTrue(False)
            return
        self.wynnrepo.online_players_repository._TABLE_NAME = "temp_online_players"  # type: ignore
        try:
            await self.wynnrepo.online_players_repository.create_table()
            t1 = perf_counter()
            l = OnlinePlayers.from_response(self.mock_onlineuuids)
            affectedrows = await self.wynnrepo.online_players_repository.insert(l)
            t2 = perf_counter()
            logger.success(f"inserted {len(l)} rows in {t2 - t1} seconds")
            self.assertGreaterEqual(affectedrows, 0)
        except Exception:
            raise
        finally:
            await self.wynnrepo.wynndb.execute("DROP TABLE temp_online_players")

    @unittest.skip("Needs long and time-consuming process to test.")
    async def test_player_activity_history_repo(self) -> None:
        pass
        # if self.toTest_guildStats is None:
        #     self.assertTrue(False)
        #     return
        # self.wynnrepo.player_activity_history_repository._TABLE_NAME = "temp_player_activity_history"
        # try:
        #     await self.wynnrepo.player_activity_history_repository.create_table()
        #     t1 = perf_counter()
        #     l = PlayerActivityHistory.from_responses(self.toTest_guildStats)
        #     affectedrows = await self.wynnrepo.player_activity_history_repository.insert(l)
        #     t2 = perf_counter()
        #     logger.success(f"inserted {len(l)} rows in {t2 - t1} seconds")
        #     self.assertGreaterEqual(affectedrows, 0)
        # except Exception:
        #     raise
        # finally:
        #     await self.wynnrepo.wynndb.execute("DROP TABLE temp_player_activity_history")

    async def test_player_history_repo(self) -> None:
        if self.mock_playerstats is None:
            self.assertTrue(False)
            return
        self.wynnrepo.player_history_repository._TABLE_NAME = "temp_player_history"  # type: ignore
        try:
            await self.wynnrepo.player_history_repository.create_table()
            t1 = perf_counter()
            l = PlayerHistory.from_responses(self.mock_playerstats)
            affectedrows = await self.wynnrepo.player_history_repository.insert(l)
            t2 = perf_counter()
            logger.success(f"inserted {len(l)} rows in {t2 - t1} seconds")
            self.assertGreaterEqual(affectedrows, 0)
        except Exception:
            raise
        finally:
            await self.wynnrepo.wynndb.execute("DROP TABLE temp_player_history")

    async def test_player_info_repo(self) -> None:
        if self.mock_playerstats is None:
            self.assertTrue(False)
            return
        self.wynnrepo.player_info_repository._TABLE_NAME = "temp_player_info"  # type: ignore
        try:
            await self.wynnrepo.player_info_repository.create_table()
            t1 = perf_counter()
            l = PlayerInfo.from_responses(self.mock_playerstats)
            affectedrows = await self.wynnrepo.player_info_repository.insert(l)
            t2 = perf_counter()
            logger.success(f"inserted {len(l)} rows in {t2 - t1} seconds")
            self.assertGreaterEqual(affectedrows, 0)
        except Exception:
            raise
        finally:
            await self.wynnrepo.wynndb.execute("DROP TABLE temp_player_info")

    async def asyncTearDown(self) -> None:
        # await self.wynnapi.close()
        return
