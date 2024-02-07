from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from loguru import Logger
    from kans import (
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


class Database(Protocol):
    """<<interface>>

    implemented by `WynnDataDatabase`"""
    def __init__(self, config: dict[str, str], logger: Logger) -> None: ...
    @property
    def guild_history_repository(self) -> GuildHistoryTable: ...
    @property
    def guild_info_repository(self) -> GuildInfoTable: ...
    @property
    def guild_member_history_repository(self) -> GuildMemberHistoryTable: ...
    @property
    def player_activity_history_repository(self) -> PlayerActivityHistoryTable: ...
    @property
    def character_history_repository(self) -> CharacterHistoryTable: ...
    @property
    def character_info_repository(self) -> CharacterInfoTable: ...
    @property
    def player_history_repository(self) -> PlayerHistoryTable: ...
    @property
    def player_info_repository(self) -> PlayerInfoTable: ...
    @property
    def online_players_repository(self) -> OnlinePlayersTable: ...
    @property
    def wynndb(self) -> DatabaseQuery: ...
