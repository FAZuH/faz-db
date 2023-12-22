from typing import TYPE_CHECKING, List, Set, TypeAlias, TypedDict

from uuid import UUID

if TYPE_CHECKING:
    from vindicator import GuildStats, PlayerStats

Timestamp: TypeAlias = float
Username: TypeAlias = str
Uuid: TypeAlias = UUID
lUsername: TypeAlias = List[Username]
lUuid: TypeAlias = List[Uuid]
sUsername: TypeAlias = Set[Username]
sUuid: TypeAlias = Set[Uuid]

FetchedPlayer = TypedDict("FetchedPlayer", {"response_timestamp": float, "player_stats": "PlayerStats"})
lFetchedPlayers: TypeAlias = List[FetchedPlayer]
lUsernames: TypeAlias = List[Username]
lUuids: TypeAlias = List[Uuid]
sUsernames: TypeAlias = Set[Username]
sUuids: TypeAlias = Set[Uuid]

FetchedGuild = TypedDict("FetchedGuild", {"response_timestamp": float, "guild_stats": "GuildStats"})
lFetchedGuilds: TypeAlias = List[FetchedGuild]
