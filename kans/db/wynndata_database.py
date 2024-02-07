from __future__ import annotations
from typing import TYPE_CHECKING, Any

from kans import (
    Database,
    DatabaseQuery,
    GuildInfoTable,
    GuildHistoryTable,
    GuildMemberHistoryTable,
    PlayerActivityHistoryTable,
    CharacterInfoTable,
    CharacterHistoryTable,
    PlayerInfoTable,
    PlayerHistoryTable,
    OnlinePlayersTable
)

if TYPE_CHECKING:
    from loguru import Logger


class WynnDataDatabase(Database):

    def __init__(self, config: dict[str, Any], logger: Logger) -> None:
        self._wynndb: DatabaseQuery = DatabaseQuery(
            config['WYNNDATA_DB_USER'], config['WYNNDATA_DB_PASSWORD'], config['WYNNDATA_DB_DBNAME'], 2
        )
        self._guild_history_repository = GuildHistoryTable(self.wynndb)
        self._guild_info_repository = GuildInfoTable(self.wynndb)
        self._guild_member_history_repository = GuildMemberHistoryTable(self.wynndb)
        self._player_activity_history_repository = PlayerActivityHistoryTable(self.wynndb)
        self._character_history_repository = CharacterHistoryTable(self.wynndb)
        self._character_info_repository = CharacterInfoTable(self.wynndb)
        self._player_history_repository = PlayerHistoryTable(self.wynndb)
        self._player_info_repository = PlayerInfoTable(self.wynndb)
        self._online_players_repository = OnlinePlayersTable(self.wynndb)

    @property
    def guild_history_repository(self) -> GuildHistoryTable:
        return self._guild_history_repository

    @property
    def guild_info_repository(self) -> GuildInfoTable:
        return self._guild_info_repository

    @property
    def guild_member_history_repository(self) -> GuildMemberHistoryTable:
        return self._guild_member_history_repository

    @property
    def player_activity_history_repository(self) -> PlayerActivityHistoryTable:
        return self._player_activity_history_repository

    @property
    def character_history_repository(self) -> CharacterHistoryTable:
        return self._character_history_repository

    @property
    def character_info_repository(self) -> CharacterInfoTable:
        return self._character_info_repository

    @property
    def player_history_repository(self) -> PlayerHistoryTable:
        return self._player_history_repository

    @property
    def player_info_repository(self) -> PlayerInfoTable:
        return self._player_info_repository

    @property
    def online_players_repository(self) -> OnlinePlayersTable:
        return self._online_players_repository

    @property
    def wynndb(self) -> DatabaseQuery:
        return self._wynndb
