from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wynndb.db.wynndb.model import (
        CharacterHistory,
        CharacterInfo,
        GuildHistory,
        GuildInfo,
        GuildMemberHistory,
        WynnDbUptime,
        OnlinePlayers,
        PlayerActivityHistory,
        PlayerHistory,
        PlayerInfo,
    )


class DbModelDictAdapter:
    """Adapter for converting database models to a dictionary."""

    @staticmethod
    def from_character_history(entity: CharacterHistory) -> CharacterHistory.Type:
        return {
                "character_uuid": entity.character_uuid.uuid,
                "level": entity.level,
                "xp": entity.xp,
                "wars": entity.wars,
                "playtime": entity.playtime,
                "mobs_killed": entity.mobs_killed,
                "chests_found": entity.chests_found,
                "logins": entity.logins,
                "deaths": entity.deaths,
                "discoveries": entity.discoveries,
                "gamemode": entity.gamemode.gamemode,
                "alchemism": entity.alchemism,
                "armouring": entity.armouring,
                "cooking": entity.cooking,
                "jeweling": entity.jeweling,
                "scribing": entity.scribing,
                "tailoring": entity.tailoring,
                "weaponsmithing": entity.weaponsmithing,
                "woodworking": entity.woodworking,
                "mining": entity.mining,
                "woodcutting": entity.woodcutting,
                "farming": entity.farming,
                "fishing": entity.fishing,
                "dungeon_completions": entity.dungeon_completions,
                "quest_completions": entity.quest_completions,
                "raid_completions": entity.raid_completions,
                "datetime": entity.datetime.datetime,
                "unique_id": entity.unique_id.uuid
        }

    @staticmethod
    def from_character_info(entity: CharacterInfo) -> CharacterInfo.Type:
        return {
                "character_uuid": entity.character_uuid.uuid,
                "uuid": entity.uuid.uuid,
                "type": entity.type
        }

    @staticmethod
    def from_guild_history(entity: GuildHistory) -> GuildHistory.Type:
        return {
                "name": entity.name,
                "level": entity.level,
                "territories": entity.territories,
                "wars": entity.wars,
                "member_total": entity.member_total,
                "online_members": entity.online_members,
                "datetime": entity.datetime.datetime,
                "unique_id": entity.unique_id.uuid
        }

    @staticmethod
    def from_guild_info(entity: GuildInfo) -> GuildInfo.Type:
        return {
                "uuid": entity.uuid.uuid,
                "name": entity.name,
                "prefix": entity.prefix,
                "created": entity.created.datetime
        }

    @staticmethod
    def from_guild_member_history(entity: GuildMemberHistory) -> GuildMemberHistory.Type:
        return {
                "uuid": entity.uuid.uuid,
                "contributed": entity.contributed,
                "joined": entity.joined.datetime,
                "datetime": entity.datetime.datetime,
                "unique_id": entity.unique_id.uuid
        }

    @staticmethod
    def from_wynndb_uptime(entity: WynnDbUptime) -> WynnDbUptime.Type:
        return {
                "start_time": entity.start_time.datetime,
                "stop_time": entity.stop_time.datetime
        }

    @staticmethod
    def from_online_players(entity: OnlinePlayers) -> OnlinePlayers.Type:
        return {
                "uuid": entity.uuid.uuid,
                "server": entity.server
        }

    @staticmethod
    def from_player_activity_history(entity: PlayerActivityHistory) -> PlayerActivityHistory.Type:
        return {
                "uuid": entity.uuid.uuid,
                "logon_datetime": entity.logon_datetime.datetime,
                "logoff_datetime": entity.logoff_datetime.datetime,
        }

    @staticmethod
    def from_player_history(entity: PlayerHistory) -> PlayerHistory.Type:
        return {
                "uuid": entity.uuid.uuid,
                "username": entity.username,
                "support_rank": entity.support_rank,
                "playtime": entity.playtime,
                "guild_name": entity.guild_name,
                "guild_rank": entity.guild_rank,
                "rank": entity.rank,
                "datetime": entity.datetime.datetime,
                "unique_id": entity.unique_id.uuid
        }

    @staticmethod
    def from_player_info(entity: PlayerInfo) -> PlayerInfo.Type:
        return {
                "uuid": entity.uuid.uuid,
                "latest_username": entity.latest_username,
                "first_join": entity.first_join.datetime
        }
