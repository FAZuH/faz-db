from datetime import datetime as dt
from datetime import timedelta as td
from types import NoneType
from typing import TYPE_CHECKING
import unittest

from tests.mock_wynnapi import MockWynnApi
from vindicator import (
    BodyDateField,
    CharacterTypeField,
    GamemodeField,
    Guild,
    Player,
    UsernameOrUuidField,
    UuidField
)

if TYPE_CHECKING:
    from vindicator import (
        GuildResponse,
        PlayerResponse,
        PlayersResponse
    )


class TestResponses(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.mockwynnapi = MockWynnApi()
        self.wynnapi = self.mockwynnapi.wynnapi
        # await self.wynnapi.start()

        self.mock_guildstats: list[GuildResponse] = self.mockwynnapi.onlineguildstats  # type: ignore
        self.mock_onlineuuids: PlayersResponse = self.mockwynnapi.onlineuuids  # type: ignore
        self.mock_playerstats: list[PlayerResponse] = self.mockwynnapi.onlineplayerstats  # type: ignore

    async def test_guild_response(self) -> None:
        for guildstat in self.mock_guildstats:
            body = guildstat.body
            self.assertIsInstance(body, Guild)
            self.assertIsInstance(body.uuid, UuidField)
            self.assertIsInstance(body.name, str)
            self.assertIsInstance(body.prefix, str)
            self.assertGreaterEqual(body.level, 0)
            self.assertGreaterEqual(body.xp_percent, 0)
            self.assertGreaterEqual(body.territories, 0)
            self.assertGreaterEqual(body.wars, 0)
            # created
            self.assertIsInstance(body.created, BodyDateField)
            self.assertIsInstance(body.created.to_datetime(), dt)

            # members
            self.assertIsInstance(body.members, Guild.Members)
            self.assertGreaterEqual(body.members.total, 0)
            for rank, usernameoruuid, member_info in body.members.iter_members():
                self.assertIsInstance(rank, str)
                self.assertIsInstance(usernameoruuid, UsernameOrUuidField)
                self.assertIsInstance(usernameoruuid, UsernameOrUuidField)
                if usernameoruuid.is_uuid():
                    usernameoruuid.to_bytes()
                else:
                    self.assertIsInstance(usernameoruuid.username, str)
                # members.memberinfo
                self.assertIsInstance(member_info, Guild.Members.MemberInfo)
                if member_info.uuid is not None:
                    self.assertIsInstance(member_info.uuid, UuidField)
                    self.assertIsInstance(member_info.uuid.to_bytes(), bytes)
                else:
                    self.assertIsInstance(member_info.username, str)
                self.assertIsInstance(member_info.online, bool)
                self.assertIsInstance(member_info.server, (NoneType, str))
                self.assertGreaterEqual(member_info.contributed, 0)
                self.assertGreaterEqual(member_info.contribution_rank, 0)
                self.assertIsInstance(member_info.joined, BodyDateField)
                self.assertIsInstance(member_info.joined.to_datetime(), dt)

            self.assertGreaterEqual(body.online, 0)
            # banner
            self.assertIsInstance(body.banner, (NoneType, Guild.Banner))
            if body.banner:
                self.assertIsInstance(body.banner.base, str)
                self.assertGreaterEqual(body.banner.tier, 0)
                self.assertIsInstance(body.banner.structure, (NoneType, str))
                # banner.layerinfo
                for layer in body.banner.layers:
                    self.assertIsInstance(layer, Guild.Banner.LayerInfo)
                    self.assertIsInstance(layer.colour, str)
                    self.assertIsInstance(layer.pattern, str)

            # season_ranks
            for rank, season_rank_info in body.iter_seasonranks():
                self.assertIsInstance(rank, str)
                # season_ranks.season_rank_info
                self.assertIsInstance(season_rank_info, Guild.SeasonRankInfo)
                self.assertGreaterEqual(season_rank_info.final_territories, 0)
                self.assertGreaterEqual(season_rank_info.rating, 0)

    async def test_player_response(self) -> None:
        for playerstat in self.mock_playerstats:
            self.assertIsInstance(playerstat.get_datetime(), dt)
            self.assertIsInstance(playerstat.get_expiry_datetime(), dt)
            self.assertIsInstance(playerstat.get_expiry_timediff(), td)

            body = playerstat.body
            self.assertIsInstance(body, Player)
            self.assertIsInstance(body.username, str)
            self.assertIsInstance(body.online, bool)
            self.assertIsInstance(body.server, (NoneType, str))
            self.assertIsInstance(body.active_character, (NoneType, UuidField))
            if body.active_character is not None:
                self.assertIsInstance(body.active_character.to_bytes(), bytes)
            self.assertIsInstance(body.uuid.to_bytes(), bytes)
            self.assertIsInstance(body.rank, str)
            self.assertIsInstance(body.rank_badge, (NoneType, str))
            # legacy_rank_colour
            self.assertIsInstance(body.legacy_rank_colour, (Player.LegacyRankColour, NoneType))
            if body.legacy_rank_colour is not None:
                self.assertIsInstance(body.legacy_rank_colour.main, str)
                self.assertIsInstance(body.legacy_rank_colour.sub, str)

            self.assertIsInstance(body.support_rank, (NoneType, str))
            self.assertIsInstance(body.veteran, bool)
            # first_join
            self.assertIsInstance(body.first_join, BodyDateField)
            self.assertIsInstance(body.first_join.to_datetime(), dt)

            # last_join
            self.assertIsInstance(body.last_join, BodyDateField)
            self.assertIsInstance(body.last_join.to_datetime(), dt)

            self.assertGreater(body.playtime, 0)
            # guild
            if body.guild is not None:
                self.assertIsInstance(body.guild, Player.Guild)
                self.assertIsInstance(body.guild.uuid.to_bytes(), bytes)
                self.assertIsInstance(body.guild.name, str)
                self.assertIsInstance(body.guild.prefix, str)
                self.assertIsInstance(body.guild.rank, str)
                self.assertIsInstance(body.guild.rank_stars, (NoneType, str))
                if body.guild.rank_stars:
                    self.assertIn('★', body.guild.rank_stars)

            # global_data
            self.assertIsInstance(body.global_data, Player.GlobalData)
            self.assertGreaterEqual(body.global_data.wars, 0)
            self.assertGreaterEqual(body.global_data.total_level, 0)
            self.assertGreaterEqual(body.global_data.killed_mobs, 0)
            self.assertGreaterEqual(body.global_data.chests_found, 0)
            # global_data.dungeons
            self.assertIsInstance(body.global_data.dungeons, Player.Dungeons)
            self.assertGreaterEqual(body.global_data.dungeons.total, 0)
            self.assertIsInstance(body.global_data.dungeons.list, dict)
            # global_data.raids
            self.assertIsInstance(body.global_data.raids, Player.Raids)
            self.assertGreaterEqual(body.global_data.raids.total, 0)
            self.assertIsInstance(body.global_data.raids.list, dict)
            # global_data.completed_quests
            self.assertGreaterEqual(body.global_data.completed_quests, 0)
            # global_data.pvp
            self.assertIsInstance(body.global_data.pvp, Player.Pvp)
            self.assertGreaterEqual(body.global_data.pvp.kills, 0)
            self.assertGreaterEqual(body.global_data.pvp.deaths, 0)

            self.assertIsInstance(body.ranking, dict)
            self.assertIsInstance(body.public_profile, bool)
            self.assertIsInstance(body.characters, dict)

            # characters
            for ch_uuid, ch in body.iter_characters():
                self.assertIsInstance(ch_uuid, UuidField)
                self.assertIsInstance(ch_uuid.to_bytes(), bytes)
                self.assertIsInstance(ch, Player.Character)
                self.assertIsInstance(ch.type, CharacterTypeField)
                self.assertIn(ch.type.get_kind(), ("MAGE", "ARCHER", "WARRIOR", "ASSASSIN", "SHAMAN"))
                self.assertIsInstance(ch.nickname, (NoneType, str))
                self.assertTrue(ch.level >= 0 and ch.level <= 106)
                self.assertGreaterEqual(ch.xp, 0)
                self.assertGreaterEqual(ch.xp_percent, 0)
                self.assertGreaterEqual(ch.total_level, 0)
                self.assertGreaterEqual(ch.wars, 0)
                self.assertGreaterEqual(ch.playtime, 0)
                self.assertGreaterEqual(ch.mobs_killed, 0)
                self.assertGreaterEqual(ch.chests_found, 0)
                self.assertGreaterEqual(ch.items_identified, 0)
                self.assertIsInstance(ch.blocks_walked, int)
                self.assertGreaterEqual(ch.logins, 0)
                self.assertGreaterEqual(ch.deaths, 0)
                self.assertGreaterEqual(ch.discoveries, 0)
                self.assertIsInstance(ch.pre_economy, bool)
                # character.pvp
                self.assertIsInstance(ch.pvp, Player.Pvp)
                self.assertGreaterEqual(ch.pvp.kills, 0)
                self.assertGreaterEqual(ch.pvp.deaths, 0)
                # character.gamemode
                self.assertIsInstance(ch.gamemode, GamemodeField)
                self.assertIsInstance(ch.gamemode.to_bytes(), bytes)
                # character.skill_points
                self.assertIsInstance(ch.skill_points, Player.Character.SkillPoints)
                self.assertGreaterEqual(ch.skill_points.earth, 0)
                self.assertGreaterEqual(ch.skill_points.thunder, 0)
                self.assertGreaterEqual(ch.skill_points.water, 0)
                self.assertGreaterEqual(ch.skill_points.fire, 0)
                self.assertGreaterEqual(ch.skill_points.air, 0)
                # character.professions
                self.assertIsInstance(ch.professions, Player.Character.Professions)

                self.assertIsInstance(ch.professions.alchemism, Player.Character.Professions.ProfessionInfo)
                self.assertGreaterEqual(ch.professions.alchemism.level, 0)
                self.assertGreaterEqual(ch.professions.alchemism.xp_percent, 0)
                self.assertGreaterEqual(ch.professions.alchemism.to_float(), 0)
                self.assertIsInstance(ch.professions.armouring, Player.Character.Professions.ProfessionInfo)
                self.assertGreaterEqual(ch.professions.armouring.level, 0)
                self.assertGreaterEqual(ch.professions.armouring.xp_percent, 0)
                self.assertGreaterEqual(ch.professions.armouring.to_float(), 0)
                self.assertIsInstance(ch.professions.cooking, Player.Character.Professions.ProfessionInfo)
                self.assertGreaterEqual(ch.professions.cooking.level, 0)
                self.assertGreaterEqual(ch.professions.cooking.xp_percent, 0)
                self.assertGreaterEqual(ch.professions.cooking.to_float(), 0)
                self.assertIsInstance(ch.professions.farming, Player.Character.Professions.ProfessionInfo)
                self.assertGreaterEqual(ch.professions.farming.level, 0)
                self.assertGreaterEqual(ch.professions.farming.xp_percent, 0)
                self.assertGreaterEqual(ch.professions.farming.to_float(), 0)
                self.assertIsInstance(ch.professions.fishing, Player.Character.Professions.ProfessionInfo)
                self.assertGreaterEqual(ch.professions.fishing.level, 0)
                self.assertGreaterEqual(ch.professions.fishing.xp_percent, 0)
                self.assertGreaterEqual(ch.professions.fishing.to_float(), 0)
                self.assertIsInstance(ch.professions.jeweling, Player.Character.Professions.ProfessionInfo)
                self.assertGreaterEqual(ch.professions.jeweling.level, 0)
                self.assertGreaterEqual(ch.professions.jeweling.xp_percent, 0)
                self.assertGreaterEqual(ch.professions.jeweling.to_float(), 0)
                self.assertIsInstance(ch.professions.mining, Player.Character.Professions.ProfessionInfo)
                self.assertGreaterEqual(ch.professions.mining.level, 0)
                self.assertGreaterEqual(ch.professions.mining.xp_percent, 0)
                self.assertGreaterEqual(ch.professions.mining.to_float(), 0)
                self.assertIsInstance(ch.professions.scribing, Player.Character.Professions.ProfessionInfo)
                self.assertGreaterEqual(ch.professions.scribing.level, 0)
                self.assertGreaterEqual(ch.professions.scribing.xp_percent, 0)
                self.assertGreaterEqual(ch.professions.scribing.to_float(), 0)
                self.assertIsInstance(ch.professions.tailoring, Player.Character.Professions.ProfessionInfo)
                self.assertGreaterEqual(ch.professions.tailoring.level, 0)
                self.assertGreaterEqual(ch.professions.tailoring.xp_percent, 0)
                self.assertGreaterEqual(ch.professions.tailoring.to_float(), 0)
                self.assertIsInstance(ch.professions.weaponsmithing, Player.Character.Professions.ProfessionInfo)
                self.assertGreaterEqual(ch.professions.weaponsmithing.level, 0)
                self.assertGreaterEqual(ch.professions.weaponsmithing.xp_percent, 0)
                self.assertGreaterEqual(ch.professions.weaponsmithing.to_float(), 0)
                self.assertIsInstance(ch.professions.woodcutting, Player.Character.Professions.ProfessionInfo)
                self.assertGreaterEqual(ch.professions.woodcutting.level, 0)
                self.assertGreaterEqual(ch.professions.woodcutting.xp_percent, 0)
                self.assertGreaterEqual(ch.professions.woodcutting.to_float(), 0)
                self.assertIsInstance(ch.professions.woodworking, Player.Character.Professions.ProfessionInfo)
                self.assertGreaterEqual(ch.professions.woodworking.level, 0)
                self.assertGreaterEqual(ch.professions.woodworking.xp_percent, 0)
                self.assertGreaterEqual(ch.professions.woodworking.to_float(), 0)

                # character.dungeons
                self.assertIsInstance(ch.dungeons, Player.Dungeons)
                self.assertGreaterEqual(ch.dungeons.total, 0)
                self.assertIsInstance(ch.dungeons.list, dict)

                # character.raids
                self.assertIsInstance(ch.raids, Player.Raids)
                self.assertGreaterEqual(ch.raids.total, 0)
                self.assertIsInstance(ch.raids.list, dict)

                self.assertIsInstance(ch.quests, list)

    async def test_players_response(self) -> None:
        players = self.mock_onlineuuids
        self.assertGreaterEqual(players.body.total, 0)
        self.assertIsInstance(players.body.players, dict)
        for usernameoruuid, server in players.body.iter_players():
            self.assertIsInstance(usernameoruuid, UsernameOrUuidField)
            if usernameoruuid.is_uuid():
                usernameoruuid.to_bytes()
            else:
                self.assertIsInstance(usernameoruuid.username, str)
            self.assertIsInstance(server, str)

    async def asyncTearDown(self) -> None:
        # await self.wynnapi.close()
        return
