from datetime import datetime as dt
from datetime import timedelta as td
import unittest
from unittest.mock import MagicMock

from tests.fixtures_api import FixturesApi
from wynndb.config import Config
from wynndb.db import DatabaseQuery
from wynndb.db.wynndb import WynnDbDatabase
from wynndb.db.wynndb.model import WynnDbUptime
from wynndb.util import ApiResponseAdapter


class TestDbRepositoryInsertFromfixture(unittest.IsolatedAsyncioTestCase):
    """Tests if db.repositories is able to insert data into database."""

    async def asyncSetUp(self) -> None:
        Config.load_config()
        self.adapter = ApiResponseAdapter()  # type: ignore

        wynndb_query = DatabaseQuery(
            Config.get_db_username(),
            Config.get_db_password(),
            Config.get_schema_name(),
            Config.get_db_max_retries()
        )
        self.db = WynnDbDatabase(MagicMock(), wynndb_query)

        fixtures = FixturesApi()
        self.mock_guildstats = fixtures.get_guilds()
        self.mock_onlineuuids = fixtures.get_online_uuids()
        self.mock_playerstats = fixtures.get_players()

    async def test_character_history_repository(self) -> None:
        self.db.character_history_repository._TABLE_NAME = "temp_character_history"  # type: ignore
        try:
            await self.db.character_history_repository.create_table()
            to_test = []
            for stat in self.mock_playerstats:
                to_test.extend(self.adapter.Player.to_character_history(stat))
            affectedrows = await self.db.character_history_repository.insert(to_test)
            self.assertGreaterEqual(affectedrows, 0)
        finally:
            await self.db.query.execute("DROP TABLE temp_character_history")

    async def test_character_info_repository(self) -> None:
        self.db.character_info_repository._TABLE_NAME = "temp_character_info"  # type: ignore
        try:
            await self.db.character_info_repository.create_table()
            to_test = []
            for stat in self.mock_playerstats:
                to_test.extend(self.adapter.Player.to_character_info(stat))
            affectedrows = await self.db.character_info_repository.insert(to_test)
            self.assertGreaterEqual(affectedrows, 0)
        finally:
            await self.db.query.execute("DROP TABLE temp_character_info")

    async def test_guild_history_repository(self) -> None:
        self.db.guild_history_repository._TABLE_NAME = "temp_guild_history"  # type: ignore
        try:
            await self.db.guild_history_repository.create_table()
            to_test = [
                    self.adapter.Guild.to_guild_history(stat)
                    for stat in self.mock_guildstats
            ]
            affectedrows = await self.db.guild_history_repository.insert(to_test)
            self.assertGreaterEqual(affectedrows, 0)
        finally:
            await self.db.query.execute("DROP TABLE temp_guild_history")

    async def test_guild_info_repository(self) -> None:
        self.db.guild_info_repository._TABLE_NAME = "temp_guild_info"  # type: ignore
        try:
            await self.db.guild_info_repository.create_table()
            to_test = [
                    self.adapter.Guild.to_guild_info(stat)
                    for stat in self.mock_guildstats
            ]
            affectedrows = await self.db.guild_info_repository.insert(to_test)
            self.assertGreaterEqual(affectedrows, 0)
        finally:
            await self.db.query.execute("DROP TABLE temp_guild_info")

    async def test_guild_member_history_repository(self) -> None:
        self.db.guild_member_history_repository._TABLE_NAME = "temp_guild_member_history"  # type: ignore
        try:
            await self.db.guild_member_history_repository.create_table()
            to_test = []
            for stat in self.mock_guildstats:
                to_test.extend(self.adapter.Guild.to_guild_member_history(stat))
            affectedrows = await self.db.guild_member_history_repository.insert(to_test)
            self.assertGreaterEqual(affectedrows, 0)
        finally:
            await self.db.query.execute("DROP TABLE temp_guild_member_history")

    async def test_wynndb_uptime_repository(self) -> None:
        self.db.wynndb_uptime_repository._TABLE_NAME = "temp_wynndb_uptime"  # type: ignore
        try:
            await self.db.wynndb_uptime_repository.create_table()
            affectedrows = await self.db.wynndb_uptime_repository.insert([WynnDbUptime(
                    dt.now(),
                    dt.now() + td(days=1.0)
            )])
            self.assertGreaterEqual(affectedrows, 0)
        finally:
            await self.db.query.execute("DROP TABLE temp_wynndb_uptime")

    async def test_online_players_repository(self) -> None:
        self.db.online_players_repository._TABLE_NAME = "temp_online_players"  # type: ignore
        try:
            await self.db.online_players_repository.create_table()
            to_test = self.adapter.OnlinePlayers.to_online_players(self.mock_onlineuuids)
            affectedrows = await self.db.online_players_repository.insert(to_test)
            self.assertGreaterEqual(affectedrows, 0)
        finally:
            await self.db.query.execute("DROP TABLE temp_online_players")

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
        self.db.player_history_repository._TABLE_NAME = "temp_player_history"  # type: ignore
        try:
            await self.db.player_history_repository.create_table()
            to_test = [
                    self.adapter.Player.to_player_history(stat)
                    for stat in self.mock_playerstats
            ]
            affectedrows = await self.db.player_history_repository.insert(to_test)
            self.assertGreaterEqual(affectedrows, 0)
        finally:
            await self.db.query.execute("DROP TABLE temp_player_history")

    async def test_player_info_repository(self) -> None:
        self.db.player_info_repository._TABLE_NAME = "temp_player_info"  # type: ignore
        try:
            await self.db.player_info_repository.create_table()
            to_test = [
                    self.adapter.Player.to_player_info(stat)
                    for stat in self.mock_playerstats
            ]
            affectedrows = await self.db.player_info_repository.insert(to_test)
            self.assertGreaterEqual(affectedrows, 0)
        finally:
            await self.db.query.execute("DROP TABLE temp_player_info")
