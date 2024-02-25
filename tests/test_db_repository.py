from datetime import datetime as dt
from datetime import timedelta as td
import unittest

from loguru import logger

from kans import config
from kans.api.wynn.response import PlayerResponse, OnlinePlayers, GuildResponse
from kans.db import Database, KansDatabase
from kans.db.model import KansUptime
from kans.heartbeat.task.task_kans_db_logger import _Converter  # type: ignore
from tests.mock_wynnapi import MockWynnApi


class TestDbRepository(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        self.converter = _Converter(None)  # type: ignore
        self.mockwynnapi = MockWynnApi()
        self.wynnrepo: Database = KansDatabase(config, logger)

        self.mock_guildstats: list[GuildResponse] = self.mockwynnapi.onlineguildstats  # type: ignore
        self.mock_onlineuuids: OnlinePlayers = self.mockwynnapi.onlineuuids  # type: ignore
        self.mock_playerstats: list[PlayerResponse] = self.mockwynnapi.onlineplayerstats  # type: ignore

    async def test_character_history_repository(self) -> None:
        self.wynnrepo.character_history_repository._TABLE_NAME = "temp_character_history"  # type: ignore
        try:
            await self.wynnrepo.character_history_repository.create_table()
            l = self.converter.to_character_history(self.mock_playerstats)
            affectedrows = await self.wynnrepo.character_history_repository.insert(l)
            self.assertGreaterEqual(affectedrows, 0)
        finally:
            await self.wynnrepo.wynndb.execute("DROP TABLE temp_character_history")

    async def test_character_info_repository(self) -> None:
        self.wynnrepo.character_info_repository._TABLE_NAME = "temp_character_info"  # type: ignore
        try:
            await self.wynnrepo.character_info_repository.create_table()
            l = self.converter.to_character_info(self.mock_playerstats)
            affectedrows = await self.wynnrepo.character_info_repository.insert(l)
            self.assertGreaterEqual(affectedrows, 0)
        finally:
            await self.wynnrepo.wynndb.execute("DROP TABLE temp_character_info")

    async def test_guild_history_repository(self) -> None:
        self.wynnrepo.guild_history_repository._TABLE_NAME = "temp_guild_history"  # type: ignore
        try:
            await self.wynnrepo.guild_history_repository.create_table()
            l = self.converter.to_guild_history(self.mock_guildstats)
            affectedrows = await self.wynnrepo.guild_history_repository.insert(l)
            self.assertGreaterEqual(affectedrows, 0)
        finally:
            await self.wynnrepo.wynndb.execute("DROP TABLE temp_guild_history")

    async def test_guild_info_repository(self) -> None:
        self.wynnrepo.guild_info_repository._TABLE_NAME = "temp_guild_info"  # type: ignore
        try:
            await self.wynnrepo.guild_info_repository.create_table()
            l = self.converter.to_guild_info(self.mock_guildstats)
            affectedrows = await self.wynnrepo.guild_info_repository.insert(l)
            self.assertGreaterEqual(affectedrows, 0)
        finally:
            await self.wynnrepo.wynndb.execute("DROP TABLE temp_guild_info")

    async def test_guild_member_history_repository(self) -> None:
        self.wynnrepo.guild_member_history_repository._TABLE_NAME = "temp_guild_member_history"  # type: ignore
        try:
            await self.wynnrepo.guild_member_history_repository.create_table()
            l = self.converter.to_guild_member_history(self.mock_guildstats)
            affectedrows = await self.wynnrepo.guild_member_history_repository.insert(l)
            self.assertGreaterEqual(affectedrows, 0)
        finally:
            await self.wynnrepo.wynndb.execute("DROP TABLE temp_guild_member_history")

    async def test_kans_uptime_repository(self) -> None:
        self.wynnrepo.kans_uptime_repository._TABLE_NAME = "temp_kans_uptime"  # type: ignore
        try:
            await self.wynnrepo.kans_uptime_repository.create_table()
            affectedrows = await self.wynnrepo.kans_uptime_repository.insert([KansUptime(
                    dt.now(),
                    dt.now() + td(days=1.0)
            )])
            self.assertGreaterEqual(affectedrows, 0)
        finally:
            await self.wynnrepo.wynndb.execute("DROP TABLE temp_kans_uptime")

    async def test_online_players_repository(self) -> None:
        self.wynnrepo.online_players_repository._TABLE_NAME = "temp_online_players"  # type: ignore
        try:
            await self.wynnrepo.online_players_repository.create_table()
            l = self.converter.to_online_players((self.mock_onlineuuids,))
            affectedrows = await self.wynnrepo.online_players_repository.insert(l)
            self.assertGreaterEqual(affectedrows, 0)
        finally:
            await self.wynnrepo.wynndb.execute("DROP TABLE temp_online_players")

    @unittest.skip("Needs long and time-consuming process to test.")
    async def test_player_activity_history_repository(self) -> None:
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

    async def test_player_history_repository(self) -> None:
        self.wynnrepo.player_history_repository._TABLE_NAME = "temp_player_history"  # type: ignore
        try:
            await self.wynnrepo.player_history_repository.create_table()
            l = self.converter.to_player_history(self.mock_playerstats)
            affectedrows = await self.wynnrepo.player_history_repository.insert(l)
            self.assertGreaterEqual(affectedrows, 0)
        finally:
            await self.wynnrepo.wynndb.execute("DROP TABLE temp_player_history")

    async def test_player_info_repository(self) -> None:
        self.wynnrepo.player_info_repository._TABLE_NAME = "temp_player_info"  # type: ignore
        try:
            await self.wynnrepo.player_info_repository.create_table()
            l = self.converter.to_player_info(self.mock_playerstats)
            affectedrows = await self.wynnrepo.player_info_repository.insert(l)
            self.assertGreaterEqual(affectedrows, 0)
        finally:
            await self.wynnrepo.wynndb.execute("DROP TABLE temp_player_info")
