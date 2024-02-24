from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from loguru import Logger
    from kans import (
        CharacterInfoRepository,
        CharacterHistoryRepository,
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


class Database(Protocol):
    """<<interface>>

    implemented by `WynnDataDatabase`"""
    def __init__(self, config: dict[str, str], logger: Logger) -> None: ...
    @property
    def character_history_repository(self) -> CharacterHistoryRepository: ...
    @property
    def character_info_repository(self) -> CharacterInfoRepository: ...
    @property
    def guild_history_repository(self) -> GuildHistoryRepository: ...
    @property
    def guild_info_repository(self) -> GuildInfoRepository: ...
    @property
    def guild_member_history_repository(self) -> GuildMemberHistoryRepository: ...
    @property
    def kans_uptime_repository(self) -> KansUptimeRepository: ...
    @property
    def online_players_repository(self) -> OnlinePlayersRepository: ...
    @property
    def player_activity_history_repository(self) -> PlayerActivityHistoryRepository: ...
    @property
    def player_history_repository(self) -> PlayerHistoryRepository: ...
    @property
    def player_info_repository(self) -> PlayerInfoRepository: ...
    @property
    def wynndb(self) -> DatabaseQuery: ...
