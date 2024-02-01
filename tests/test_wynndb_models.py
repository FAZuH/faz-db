from datetime import datetime as dt
from decimal import Decimal
from types import NoneType
import unittest

# from tests import vcr
from tests.mock_wynnapi import MockWynnApi
from vindicator import (
    CharacterHistory,
    CharacterInfo,
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

        self.toTest_guildStats: list[GuildResponse] = self.mockwynnapi.onlineGuildStats  # type: ignore
        self.toTest_onlineUuids: PlayersResponse = self.mockwynnapi.onlineUuids  # type: ignore
        self.toTest_playerStats: list[PlayerResponse] = self.mockwynnapi.onlinePlayerStats  # type: ignore

    # @vcr.use_cassette
    async def test_character_history(self) -> None:
        for playerStat in self.toTest_playerStats:
            char_hist = CharacterHistory.from_response(playerStat)
            for row in char_hist:
                self.assertIsInstance(row, CharacterHistory)
                self.assertIsInstance(row.character_uuid, UuidColumn)
                self.assertIsInstance(row.level, int)
                self.assertIsInstance(row.xp, int)
                self.assertIsInstance(row.wars, int)
                self.assertIsInstance(row.playtime, Decimal)
                self.assertIsInstance(row.mobs_killed, int)
                self.assertIsInstance(row.chests_found, int)
                self.assertIsInstance(row.logins, int)
                self.assertIsInstance(row.deaths, int)
                self.assertIsInstance(row.discoveries, int)
                self.assertIsInstance(row.gamemode, GamemodeColumn)
                self.assertIsInstance(row.alchemism, Decimal)
                self.assertIsInstance(row.armouring, Decimal)
                self.assertIsInstance(row.cooking, Decimal)
                self.assertIsInstance(row.jeweling, Decimal)
                self.assertIsInstance(row.scribing, Decimal)
                self.assertIsInstance(row.tailoring, Decimal)
                self.assertIsInstance(row.weaponsmithing, Decimal)
                self.assertIsInstance(row.woodworking, Decimal)
                self.assertIsInstance(row.mining, Decimal)
                self.assertIsInstance(row.woodcutting, Decimal)
                self.assertIsInstance(row.farming, Decimal)
                self.assertIsInstance(row.fishing, Decimal)
                self.assertIsInstance(row.dungeon_completions, int)
                self.assertIsInstance(row.quest_completions, int)
                self.assertIsInstance(row.raid_completions, int)
                self.assertIsInstance(row.datetime, dt)

    # @vcr.use_cassette
    async def test_character_info(self) -> None:
        for playerStat in self.toTest_playerStats:
            char_inf = CharacterInfo.from_response(playerStat)
            for row in char_inf:
                # assert instance of row members
                self.assertIsInstance(row.character_uuid, UuidColumn)
                self.assertIsInstance(row.uuid, UuidColumn)
                self.assertIsInstance(row.type, str)

    # @vcr.use_cassette
    async def test_guild_history(self) -> None:
        for guildStats in self.toTest_guildStats:
            guild_hist = GuildHistory.from_response(guildStats)
            self.assertIsInstance(guild_hist.name, str)
            self.assertIsInstance(guild_hist.level, Decimal)
            self.assertIsInstance(guild_hist.territories, int)
            self.assertIsInstance(guild_hist.wars, int)
            self.assertIsInstance(guild_hist.member_total, int)
            self.assertIsInstance(guild_hist.online_members, int)
            self.assertIsInstance(guild_hist.datetime, dt)

    # @vcr.use_cassette
    async def test_guild_info(self) -> None:
        for guildStats in self.toTest_guildStats:
            guild_info = GuildInfo.from_response(guildStats)
            self.assertIsInstance(guild_info.name, str)
            self.assertIsInstance(guild_info.prefix, str)
            self.assertIsInstance(guild_info.created, dt)

    # @vcr.use_cassette
    async def test_guild_member_history(self) -> None:
        for guildStats in self.toTest_guildStats:
            guild_member_history = GuildMemberHistory.from_response(guildStats)
            for row in guild_member_history:
                self.assertIsInstance(row.uuid, UuidColumn)
                self.assertIsInstance(row.contributed, int)
                self.assertIsInstance(row.joined, dt)
                self.assertIsInstance(row.datetime, dt)

    # @vcr.use_cassette
    async def test_online_players(self) -> None:
        online_players = OnlinePlayers.from_response(self.toTest_onlineUuids)
        for row in online_players:
            self.assertIsInstance(row.uuid, UuidColumn)
            self.assertIsInstance(row.server, str)

    @unittest.skip("Needs long and time-consuming process to test.")
    async def test_player_activity_history(self) -> None:
        pass

    # @vcr.use_cassette
    async def test_player_history(self) -> None:
        for playerStat in self.toTest_playerStats:
            player_history = PlayerHistory.from_response(playerStat)
            self.assertIsInstance(player_history.uuid, UuidColumn)
            self.assertIsInstance(player_history.username, str)
            self.assertIsInstance(player_history.support_rank, (NoneType, str))
            self.assertIsInstance(player_history.playtime, Decimal)
            self.assertIsInstance(player_history.guild_name, (NoneType, str))
            self.assertIsInstance(player_history.guild_rank, (NoneType, str))
            self.assertIsInstance(player_history.rank, str)
            self.assertIsInstance(player_history.datetime, dt)

    # @vcr.use_cassette
    async def test_player_info(self) -> None:
        for playerStat in self.toTest_playerStats:
            player_info = PlayerInfo.from_model(playerStat)
            self.assertIsInstance(player_info.uuid, UuidColumn)
            self.assertIsInstance(player_info.latest_username, str)
            self.assertIsInstance(player_info.first_join, dt)

    async def asyncTearDown(self) -> None:
        # await self.wynnapi.close()
        return
