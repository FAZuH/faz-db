from __future__ import annotations
from typing import TYPE_CHECKING

from kans import (
    CharacterInfoRepository,
    CharacterHistoryRepository,
    Database,
    DatabaseQuery,
    GuildInfoRepository,
    GuildHistoryRepository,
    GuildMemberHistoryRepository,
    KansUptimeRepository,
    OnlinePlayersRepository,
    PlayerActivityHistoryRepository,
    PlayerInfoRepository,
    PlayerHistoryRepository,
)

if TYPE_CHECKING:
    from loguru import Logger
    from constants import ConfigT


class WynnDataDatabase(Database):

    def __init__(self, config: ConfigT, logger: Logger) -> None:
        self._wynndb: DatabaseQuery = DatabaseQuery(
            config['WYNNDATA_DB_USER'], config['WYNNDATA_DB_PASSWORD'], config['WYNNDATA_SCHEMA_NAME'], 2
        )
        self._character_history_repository = CharacterHistoryRepository(self.wynndb)
        self._character_info_repository = CharacterInfoRepository(self.wynndb)
        self._guild_history_repository = GuildHistoryRepository(self.wynndb)
        self._guild_info_repository = GuildInfoRepository(self.wynndb)
        self._guild_member_history_repository = GuildMemberHistoryRepository(self.wynndb)
        self._kans_uptime_repository = KansUptimeRepository(self.wynndb)
        self._online_players_repository = OnlinePlayersRepository(self.wynndb)
        self._player_activity_history_repository = PlayerActivityHistoryRepository(self.wynndb)
        self._player_history_repository = PlayerHistoryRepository(self.wynndb)
        self._player_info_repository = PlayerInfoRepository(self.wynndb)

    @property
    def guild_history_repository(self) -> GuildHistoryRepository:
        return self._guild_history_repository

    @property
    def guild_info_repository(self) -> GuildInfoRepository:
        return self._guild_info_repository

    @property
    def guild_member_history_repository(self) -> GuildMemberHistoryRepository:
        return self._guild_member_history_repository

    @property
    def kans_uptime_repository(self) -> KansUptimeRepository:
        return self._kans_uptime_repository

    @property
    def player_activity_history_repository(self) -> PlayerActivityHistoryRepository:
        return self._player_activity_history_repository

    @property
    def character_history_repository(self) -> CharacterHistoryRepository:
        return self._character_history_repository

    @property
    def character_info_repository(self) -> CharacterInfoRepository:
        return self._character_info_repository

    @property
    def player_history_repository(self) -> PlayerHistoryRepository:
        return self._player_history_repository

    @property
    def player_info_repository(self) -> PlayerInfoRepository:
        return self._player_info_repository

    @property
    def online_players_repository(self) -> OnlinePlayersRepository:
        return self._online_players_repository

    @property
    def wynndb(self) -> DatabaseQuery:
        return self._wynndb
