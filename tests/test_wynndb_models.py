from decimal import Decimal
from types import NoneType
import unittest

# from tests import vcr
from tests.mock_wynnapi import MockWynnApi
from vindicator import (
    CharacterHistory,
    CharacterInfo,
    DateColumn,
    GamemodeColumn,
    GuildHistory,
    GuildResponse,
    GuildInfo,
    GuildMemberHistory,
    OnlinePlayers,
    # PlayerActivityHistory,
    PlayerHistory,
    PlayerInfo,
    PlayerResponse,
    PlayersResponse,
    UuidColumn,
)


class TestWynnDbModels(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.mockwynnapi = MockWynnApi()
        self.wynnapi = self.mockwynnapi.wynnapi
        # await self.wynnapi.start()

        self.mock_guildstats: list[GuildResponse] = self.mockwynnapi.onlineguildstats  # type: ignore
        self.mock_onlineuuids: PlayersResponse = self.mockwynnapi.onlineuuids  # type: ignore
        self.mock_playerstats: list[PlayerResponse] = self.mockwynnapi.onlineplayerstats  # type: ignore

    # @vcr.use_cassette
    async def test_character_history(self) -> None:
        for char_hist in CharacterHistory.from_responses(self.mock_playerstats):
            self.assertIsInstance(char_hist, CharacterHistory)
            self.assertIsInstance(char_hist.character_uuid, UuidColumn)
            self.assertIsInstance(char_hist.level, int)
            self.assertIsInstance(char_hist.xp, int)
            self.assertIsInstance(char_hist.wars, int)
            self.assertIsInstance(char_hist.playtime, Decimal)
            self.assertIsInstance(char_hist.mobs_killed, int)
            self.assertIsInstance(char_hist.chests_found, int)
            self.assertIsInstance(char_hist.logins, int)
            self.assertIsInstance(char_hist.deaths, int)
            self.assertIsInstance(char_hist.discoveries, int)
            self.assertIsInstance(char_hist.gamemode, GamemodeColumn)
            self.assertIsInstance(char_hist.alchemism, Decimal)
            self.assertIsInstance(char_hist.armouring, Decimal)
            self.assertIsInstance(char_hist.cooking, Decimal)
            self.assertIsInstance(char_hist.jeweling, Decimal)
            self.assertIsInstance(char_hist.scribing, Decimal)
            self.assertIsInstance(char_hist.tailoring, Decimal)
            self.assertIsInstance(char_hist.weaponsmithing, Decimal)
            self.assertIsInstance(char_hist.woodworking, Decimal)
            self.assertIsInstance(char_hist.mining, Decimal)
            self.assertIsInstance(char_hist.woodcutting, Decimal)
            self.assertIsInstance(char_hist.farming, Decimal)
            self.assertIsInstance(char_hist.fishing, Decimal)
            self.assertIsInstance(char_hist.dungeon_completions, int)
            self.assertIsInstance(char_hist.quest_completions, int)
            self.assertIsInstance(char_hist.raid_completions, int)
            self.assertIsInstance(char_hist.datetime, DateColumn)

    # @vcr.use_cassette
    async def test_character_info(self) -> None:
        for char_inf in CharacterInfo.from_responses(self.mock_playerstats):
            # assert instance of row members
            self.assertIsInstance(char_inf.character_uuid, UuidColumn)
            self.assertIsInstance(char_inf.uuid, UuidColumn)
            self.assertIsInstance(char_inf.type, str)

    # @vcr.use_cassette
    async def test_guild_history(self) -> None:
        for guild_hist in GuildHistory.from_responses(self.mock_guildstats):
            self.assertIsInstance(guild_hist.name, str)
            self.assertIsInstance(guild_hist.level, Decimal)
            self.assertIsInstance(guild_hist.territories, int)
            self.assertIsInstance(guild_hist.wars, int)
            self.assertIsInstance(guild_hist.member_total, int)
            self.assertIsInstance(guild_hist.online_members, int)
            self.assertIsInstance(guild_hist.datetime, DateColumn)

    # @vcr.use_cassette
    async def test_guild_info(self) -> None:
        for guild_info in GuildInfo.from_responses(self.mock_guildstats):
            self.assertIsInstance(guild_info.name, str)
            self.assertIsInstance(guild_info.prefix, str)
            self.assertIsInstance(guild_info.created, DateColumn)

    # @vcr.use_cassette
    async def test_guild_member_history(self) -> None:
        for guild_member_history in GuildMemberHistory.from_responses(self.mock_guildstats):
            self.assertIsInstance(guild_member_history.uuid, UuidColumn)
            self.assertIsInstance(guild_member_history.contributed, int)
            self.assertIsInstance(guild_member_history.joined, DateColumn)
            self.assertIsInstance(guild_member_history.datetime, DateColumn)

    # @vcr.use_cassette
    async def test_online_players(self) -> None:
        online_players = OnlinePlayers.from_response(self.mock_onlineuuids)
        for row in online_players:
            self.assertIsInstance(row.uuid, UuidColumn)
            self.assertIsInstance(row.server, str)

    @unittest.skip("Needs long and time-consuming process to test.")
    async def test_player_activity_history(self) -> None:
        pass

    # @vcr.use_cassette
    async def test_player_history(self) -> None:
        for player_history in PlayerHistory.from_responses(self.mock_playerstats):
            self.assertIsInstance(player_history.uuid, UuidColumn)
            self.assertIsInstance(player_history.username, str)
            self.assertIsInstance(player_history.support_rank, (NoneType, str))
            self.assertIsInstance(player_history.playtime, Decimal)
            self.assertIsInstance(player_history.guild_name, (NoneType, str))
            self.assertIsInstance(player_history.guild_rank, (NoneType, str))
            self.assertIsInstance(player_history.rank, str)
            self.assertIsInstance(player_history.datetime, DateColumn)

    # @vcr.use_cassette
    async def test_player_info(self) -> None:
        for player_info in PlayerInfo.from_responses(self.mock_playerstats):
            self.assertIsInstance(player_info.uuid, UuidColumn)
            self.assertIsInstance(player_info.latest_username, str)
            self.assertIsInstance(player_info.first_join, DateColumn)

    async def asyncTearDown(self) -> None:
        # await self.wynnapi.close()
        return
