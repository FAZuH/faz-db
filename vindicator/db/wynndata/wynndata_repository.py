from __future__ import annotations
from typing import TYPE_CHECKING

from vindicator import (
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
    from vindicator import DatabaseQuery


class WynnDataRepository:

    def __init__(self, wynndata_db: DatabaseQuery) -> None:
        self._wynndata_db = wynndata_db
        self._guild_history_repository = GuildHistoryTable(self.wynndata_db)
        self._guild_info_repository = GuildInfoTable(self.wynndata_db)
        self._guild_member_history_repository = GuildMemberHistoryTable(self.wynndata_db)
        self._player_activity_history_repository = PlayerActivityHistoryTable(self.wynndata_db)
        self._character_history_repository = CharacterHistoryTable(self.wynndata_db)
        self._character_info_repository = CharacterInfoTable(self.wynndata_db)
        self._player_history_repository = PlayerHistoryTable(self.wynndata_db)
        self._player_info_repository = PlayerInfoTable(self.wynndata_db)
        self._online_players_repository = OnlinePlayersTable(self.wynndata_db)

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
    def wynndata_db(self) -> DatabaseQuery:
        return self._wynndata_db
