from __future__ import annotations
from datetime import datetime
from typing import Generator, TYPE_CHECKING

from fazdb.db.fazdb.model import (
    CharacterHistory,
    CharacterInfo,
    GuildHistory,
    GuildInfo,
    GuildMemberHistory,
    OnlinePlayers,
    PlayerActivityHistory,
    PlayerHistory,
    PlayerInfo,
    Worlds,
)

if TYPE_CHECKING:
    from fazdb.api.wynn.response import GuildResponse, OnlinePlayersResponse, PlayerResponse


class ApiResponseAdapter:
    """Adapter for converting wynncraft API responses to DB models."""

    class Player:

        @staticmethod
        def to_character_history(resp: PlayerResponse) -> Generator[CharacterHistory, None, None]:
            return (CharacterHistory(
                character_uuid=ch_uuid.to_bytes(),
                level=ch.level,
                xp=ch.xp,
                wars=ch.wars,
                playtime=ch.playtime,
                mobs_killed=ch.mobs_killed,
                chests_found=ch.chests_found,
                logins=ch.logins,
                deaths=ch.deaths,
                discoveries=ch.discoveries,
                hardcore=ch.gamemode.is_hardcore,
                ultimate_ironman=ch.gamemode.is_ultimate_ironman,
                ironman=ch.gamemode.is_ironman,
                craftsman=ch.gamemode.is_craftsman,
                hunted=ch.gamemode.is_hunted,
                alchemism=ch.professions.alchemism.to_decimal(),
                armouring=ch.professions.armouring.to_decimal(),
                cooking=ch.professions.cooking.to_decimal(),
                jeweling=ch.professions.jeweling.to_decimal(),
                scribing=ch.professions.scribing.to_decimal(),
                tailoring=ch.professions.tailoring.to_decimal(),
                weaponsmithing=ch.professions.weaponsmithing.to_decimal(),
                woodworking=ch.professions.woodworking.to_decimal(),
                mining=ch.professions.mining.to_decimal(),
                woodcutting=ch.professions.woodcutting.to_decimal(),
                farming=ch.professions.farming.to_decimal(),
                fishing=ch.professions.fishing.to_decimal(),
                dungeon_completions=ch.dungeons.total,
                quest_completions=len(ch.quests),
                raid_completions=ch.raids.total,
                datetime=resp.headers.to_datetime()
            ) for ch_uuid, ch in resp.body.iter_characters())

        @staticmethod
        def to_character_info(resp: PlayerResponse) -> Generator[CharacterInfo, None, None]:
            return (CharacterInfo(
                character_uuid=character_uuid.to_bytes(),
                uuid=resp.body.uuid.to_bytes(),
                type=character.type.get_kind_str()
            ) for character_uuid, character in resp.body.iter_characters())

        @staticmethod
        def to_player_history(resp: PlayerResponse) -> PlayerHistory:
            return PlayerHistory(
                uuid=resp.body.uuid.to_bytes(),
                username=resp.body.username,
                support_rank=resp.body.support_rank,
                playtime=resp.body.playtime,
                guild_name=resp.body.guild.name if resp.body.guild else None,
                guild_rank=resp.body.guild.rank if resp.body.guild else None,
                rank=resp.body.rank,
                datetime=resp.headers.to_datetime()
            )

        @staticmethod
        def to_player_info(resp: PlayerResponse) -> PlayerInfo:
            return PlayerInfo(
                uuid=resp.body.uuid.to_bytes(),
                latest_username=resp.body.username,
                first_join=resp.body.first_join.to_datetime()
            )

    class Guild:

        @staticmethod
        def to_guild_history(resp: GuildResponse) -> GuildHistory:
            return GuildHistory(
                name=resp.body.name,
                level=resp.body.level,
                territories=resp.body.territories,
                wars=resp.body.wars,
                member_total=resp.body.members.total,
                online_members=resp.body.members.get_online_members(),
                datetime=resp.headers.to_datetime()
            )

        @staticmethod
        def to_guild_info(resp: GuildResponse) -> GuildInfo:
            return GuildInfo(
                uuid=resp.body.uuid.to_bytes(),
                name=resp.body.name,
                prefix=resp.body.prefix,
                created=resp.body.created.to_datetime()
            )

        @staticmethod
        def to_guild_member_history(resp: GuildResponse) -> Generator[GuildMemberHistory, None, None]:
            return (GuildMemberHistory(
                uuid=uuid.to_bytes() if uuid.is_uuid() else memberinfo.uuid.to_bytes(),  # type: ignore
                contributed=memberinfo.contributed,
                joined=memberinfo.joined.to_datetime(),
                datetime=resp.headers.to_datetime()
            ) for rank, uuid, memberinfo in resp.body.members.iter_online_members())  # type: ignore

    class OnlinePlayers:

        @staticmethod
        def to_online_players(resp: OnlinePlayersResponse) -> Generator[OnlinePlayers, None, None]:
            return (OnlinePlayers(uuid=uuid.to_bytes(), server=server) for uuid, server in resp.body.iter_players())

        @staticmethod
        def to_player_activity_history(
            resp: OnlinePlayersResponse,
            logon_timestamps: dict[str, datetime]
        ) -> Generator[PlayerActivityHistory, None, None]:
            return (
                PlayerActivityHistory(
                    uuid=uuid.to_bytes(),  # the user's uuid
                    logon_datetime=logon_timestamps[uuid.username_or_uuid],  # when did the user logged on
                    logoff_datetime=resp.headers.to_datetime()  # the response timestamp
                )
                for uuid in resp.body.players
                if uuid.is_uuid() is True
            )
        
        @staticmethod
        def to_worlds(resp: OnlinePlayersResponse) -> Generator[Worlds, None, None]:
            worldlist: dict[str, int] = {}
            for _, world in resp.body.iter_players():
                if world not in worldlist:
                    worldlist[world] = 0
                else:
                    worldlist[world] += 1
            for world, player_count in worldlist.items():
                yield Worlds(
                    name=world,
                    player_count=player_count,
                    time_created=datetime.now(),
                )
