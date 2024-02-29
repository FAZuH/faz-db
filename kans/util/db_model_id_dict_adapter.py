from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from kans.db.model import (
        CharacterHistoryId,
        CharacterInfoId,
        GuildHistoryId,
        GuildInfoId,
        GuildMemberHistoryId,
        KansUptimeId,
        OnlinePlayersId,
        PlayerActivityHistoryId,
        PlayerHistoryId,
        PlayerInfoId,
    )


class DbModelIdDictAdapter:
    """Adapter for converting database id models to a dictionary."""

    @staticmethod
    def from_character_history(entity: CharacterHistoryId) -> CharacterHistoryId.IdType:
        return {
                "character_uuid": entity.character_uuid.uuid,
                "datetime": entity.datetime.datetime
        }

    @staticmethod
    def from_character_info(entity: CharacterInfoId) -> CharacterInfoId.IdType:
        return {
                "character_uuid": entity.character_uuid.uuid
        }

    @staticmethod
    def from_guild_history(entity: GuildHistoryId) -> GuildHistoryId.IdType:
        return {
                "name": entity.name,
                "datetime": entity.datetime.datetime
        }

    @staticmethod
    def from_guild_info(entity: GuildInfoId) -> GuildInfoId.IdType:
        return {
                "name": entity.name
        }

    @staticmethod
    def from_guild_member_history(entity: GuildMemberHistoryId) -> GuildMemberHistoryId.IdType:
        return {
                "uuid": entity.uuid.uuid,
                "datetime": entity.datetime.datetime
        }

    @staticmethod
    def from_kans_uptime(entity: KansUptimeId) -> KansUptimeId.TypeId:
        return {
                "start_time": entity.start_time.datetime
        }

    @staticmethod
    def from_online_players(entity: OnlinePlayersId) -> OnlinePlayersId.IdType:
        return {
                "uuid": entity.uuid.uuid
        }

    @staticmethod
    def from_player_activity_history(entity: PlayerActivityHistoryId) -> PlayerActivityHistoryId.IdType:
        return {
                "uuid": entity.uuid.uuid,
                "logon_datetime": entity.logon_datetime.datetime
        }

    @staticmethod
    def from_player_history(entity: PlayerHistoryId) -> PlayerHistoryId.IdType:
        return {
                "uuid": entity.uuid.uuid,
                "datetime": entity.datetime.datetime
        }

    @staticmethod
    def from_player_info(entity: PlayerInfoId) -> PlayerInfoId.IdType:
        return {
                "uuid": entity.uuid.uuid
        }
