from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from .. import Database, DatabaseQuery
from .repository import (
    CharacterInfoRepository,
    CharacterHistoryRepository,
    GuildInfoRepository,
    GuildHistoryRepository,
    GuildMemberHistoryRepository,
    KansUptimeRepository,
    OnlinePlayersRepository,
    PlayerActivityHistoryRepository,
    PlayerInfoRepository,
    PlayerHistoryRepository,
    Repository,
)
from kans.adapter import DbModelDictAdapter, DbModelIdDictAdapter

if TYPE_CHECKING:
    from kans import Config, Logger


class KansDatabase(Database):

    def __init__(self, config: Config, logger: Logger) -> None:
        self._dbquery: DatabaseQuery = DatabaseQuery(
                config.db_username,
                config.db_password,
                config.schema_name,
                2
        )
        adapter = DbModelDictAdapter()
        id_adapter = DbModelIdDictAdapter()
        self._character_history_repository = CharacterHistoryRepository(self.query, adapter, id_adapter)
        self._character_info_repository = CharacterInfoRepository(self.query, adapter, id_adapter)
        self._guild_history_repository = GuildHistoryRepository(self.query, adapter, id_adapter)
        self._guild_info_repository = GuildInfoRepository(self.query, adapter, id_adapter)
        self._guild_member_history_repository = GuildMemberHistoryRepository(self.query, adapter, id_adapter)
        self._kans_uptime_repository = KansUptimeRepository(self.query, adapter, id_adapter)
        self._online_players_repository = OnlinePlayersRepository(self.query, adapter, id_adapter)
        self._player_activity_history_repository = PlayerActivityHistoryRepository(self.query, adapter, id_adapter)
        self._player_history_repository = PlayerHistoryRepository(self.query, adapter, id_adapter)
        self._player_info_repository = PlayerInfoRepository(self.query, adapter, id_adapter)
        self._all_repositories: list[Repository[Any, Any]] = [
                self._character_history_repository,
                self._character_info_repository,
                self._guild_history_repository,
                self._guild_info_repository,
                self._guild_member_history_repository,
                self._kans_uptime_repository,
                self._online_players_repository,
                self._player_activity_history_repository,
                self._player_history_repository,
                self._player_info_repository,
        ]

    async def create_all(self) -> None:
        for repo in self._all_repositories:
            await repo.create_table()

    async def total_size(self) -> Decimal:
        sum_size = Decimal(0)
        for repo in self._all_repositories:
            sum_size += await repo.table_size()
        return sum_size

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
    def query(self) -> DatabaseQuery:
        return self._dbquery
