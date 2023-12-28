from __future__ import annotations
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, Tuple, TypedDict, TypeAlias, Union

from aiohttp import ClientResponse
from uuid import UUID

if TYPE_CHECKING:
    from asyncio import Task
    from aiomysql import Connection, Cursor
    from vindicator.request.ratelimit import Ratelimit


Rank: TypeAlias = str
Server: TypeAlias = str
Timestamp: TypeAlias = float
Username: TypeAlias = str
UsernameOrUUID: TypeAlias = str
Uuid: TypeAlias = UUID

ReturnGather: TypeAlias = Union[BaseException, ClientResponse]
Record: TypeAlias = Dict[str, Any]

lRecords: TypeAlias = List[Record]
lUsername: TypeAlias = List[Username]
lUuid: TypeAlias = List[Uuid]
sUsername: TypeAlias = Set[Username]
sUuid: TypeAlias = Set[Uuid]
tReturnGather: TypeAlias = Tuple[ReturnGather]

GuildMainInfoT = TypedDict("GuildMainInfo", {
    "created": int,  # int unsigned
    "name": str,  # varchar(30)
    "prefix": str  # varchar(4)
})
GuildMainT = TypedDict("GuildMain", {
    "level": float,  # decimal(5, 2)
    "member_total": int,  # tinyint unsigned
    "name": str,  # varchar(30)
    "online_members": int,  # tinyint unsigned
    "territories": int,  # smallint unsigned
    "wars": int,  # int unsigned

    "unique_hash": bytes,  # binary(32)
    "timestamp": int,  # int unsigned
})
GuildMemberT = TypedDict("GuildMember", {
    "joined": int,  # int unsigned
    "uuid": bytes,  # binary(16)
    "contributed": int,  # bigint unsigned

    "unique_hash": bytes,  # binary(32)
    "timestamp": int,  # int unsigned
})
PlayerActivityT = TypedDict("PlayerActivity", {
    "logoff_timestamp": int,  # NOTE: int unsigned
    "logon_timestamp": int,  # NOTE: int unsigned
    "uuid": bytes  # NOTE: binary(16)
})
PlayerCharacterInfoT = TypedDict("PlayerCharacterInfo", {
    "character_uuid": bytes,  # binary(16)
    "type": str,  # enum('ARCHER', 'ASSASSIN', 'MAGE', 'SHAMAN', 'WARRIOR')
    "uuid": bytes  # binary(16)
})
PlayerCharacterT = TypedDict(("PlayerCharacter"), {
    "character_uuid": bytes,  # binary(16)

    # Professions
    "alchemism": float,  # decimal(5, 2) unsigned
    "armouring": float,  # decimal(5, 2) unsigned
    "cooking": float,  # decimal(5, 2) unsigned
    "farming": float,  # decimal(5, 2) unsigned
    "fishing": float,  # decimal(5, 2) unsigned
    "jeweling": float,  # decimal(5, 2) unsigned
    "mining": float,  # decimal(5, 2) unsigned
    "scribing": float,  # decimal(5, 2) unsigned
    "tailoring": float,  # decimal(5, 2) unsigned
    "weaponsmithing": float,  # decimal(5, 2) unsigned
    "woodcutting": float,  # decimal(5, 2) unsigned
    "woodworking": float,  # decimal(5, 2) unsigned

    # Direct
    "chests_found": int,  # int unsigned
    "deaths": int,  # int unsigned
    "discoveries": int,  # int unsigned
    "level": float,  # decimal(5, 2) unsigned
    "logins": int,  # int unsigned
    "mobs_killed": int,  # int unsigned
    "playtime": float,  # decimal(7, 2) unsigned
    "wars": int,  # int unsigned
    "xp": int,  # bigint unsigned
    "dungeon_completions": int,  # int unsigned
    "quest_completions": int,  # int unsigned
    "raid_completions": int,  # int unsigned

    # Needs special computation
    "gamemode": bytes,  # bit(5)

    "unique_hash": bytes,  # binary(32)
    "timestamp": int,  # int unsigned
})
PlayerMainInfoT = TypedDict(("PlayerMainInfo"), {
    "first_join": Optional[int],  # int unsigned
    "latest_username": str,  # varchar(16)
    "server": Optional[str],  # varchar(10)
    "uuid": bytes,  # binary(16)
})
PlayerMainT = TypedDict("PlayerMain", {
    "guild_name": Optional[str],  # varchar(30)
    "guild_rank": Optional[str],  # enum('OWNER', 'CHIEF', 'STRATEGIST', 'CAPTAIN', 'RECRUITER', 'RECRUIT)
    "playtime": float,  # decimal(7, 2) unsigned
    "support_rank": Optional[str],  # varchar(45)
    "rank": str,  # varchar(30)
    "username": str,  # varchar(16)
    "uuid": bytes,  # binary(16)

    "unique_hash": bytes,  # binary(32)
    "timestamp": int,  # int unsigned
}, total=False)
class RawResponsesT(TypedDict):
    endpoint: str  # NOTE: enum('guild_list', 'territory_list', 'online_player_list')
    response: dict  # NOTE: json


GuildRecord = TypedDict("GuildRecord", {
    "name": str,
    "prefix": str
})
GuildList: TypeAlias = List[GuildRecord]
SeasonRankInfo = TypedDict("SeasonRanks", {
    "rating": int,
    "finalTerritories": int
})
BannerLayer = TypedDict("BannerLayer", {
    "colour": str,
    "pattern": str
})
GuildBanner = TypedDict("GuildBanner", {
    "base": str,
    "tier": int,
    "structure": str,
    "layers": List[BannerLayer]
})
GuildMemberInfo = TypedDict("GuildMember", {
    "uuid": str,
    "online": bool,
    "server": Optional[str],
    "contributed": int,
    "guildRank": int,
    "joined": str,
})
GuildMembers = TypedDict("GuildMembers", {
    "total": int,
    "owner": Dict[Username, GuildMemberInfo],
    "chief": Dict[Username, GuildMemberInfo],
    "strategist": Dict[Username, GuildMemberInfo],
    "captain": Dict[Username, GuildMemberInfo],
    "recruiter": Dict[Username, GuildMemberInfo],
    "recruit": Dict[Username, GuildMemberInfo]
})
GuildStats = TypedDict("GuildStats", {  # NOTE: Main
    "name": str,
    "prefix": str,
    "level": int,
    "xpPercent": int,
    "territories": int,
    "wars": int,
    "created": str,
    "members": GuildMembers,
    "online": int,
    "banner": GuildBanner,
    "seasonRanks": Dict[Rank, SeasonRankInfo]
})
Headers = TypedDict("Headers", {
    "Allow": str,
    "CF-Cache-Status": str,
    "CF-RAY": str,
    "Cache-Control": str,
    "Connection": str,
    "Content-Encoding": str,
    "Content-Type": str,
    "Cross-Origin-Opener-Policy": str,
    "Date": str,  # important for record info
    "Expires": str,  # important for record info
    "RateLimit-Limit": str,  # used for ratelimit manager
    "RateLimit-Remaining": str,  # used for ratelimit manager
    "RateLimit-Reset": str,  # used for ratelimit manager
    "Referrer-Policy": str,
    "Server": str,
    "Transfer-Encoding": str,
    "Vary": str,
    "Version": str,
    "Via": str,
    "WWW-Authenticate": str,
    "X-Content-Type-Options": str,
    "X-Frame-Options": str,
    "X-Kong-Proxy-Latency": str,
    "X-Kong-Upstream-Latency": str,
    "X-RateLimit-Limit-Minute": str,
    "X-RateLimit-Remaining-Minute": str,
})
OnlinePlayerList = TypedDict("OnlinePlayerList", {
    "total": int,
    "players": Dict[UsernameOrUUID, Server]
})
GuildInfo = TypedDict("GuildInfo", {
    "name": str,
    "prefix": str,
    "rank": str,
    "rankStars": str
})
DungeonList = TypedDict("DungeonList", {})  # TODO: INCOMPLETE
DungeonInfo = TypedDict("DungeonInfo", {
    "total": int,
    "list": Dict[str, int]  # TODO: INCOMPLETE
})
RaidList = TypedDict("RaidList", {})  # TODO: INCOMPLETE
RaidInfo = TypedDict("RaidInfo", {
    "total": int,
    "list": Dict[str, int]  # TODO: INCOMPLETE
})
PvpInfo = TypedDict("PvpInfo", {
    "kills": int,
    "deaths": int
})
SkillPointsInfo = TypedDict("SkillPointsInfo", {
    "strength": int,
    "dexterity": int,
    "intelligence": int,
    "defence": int,
    "agility": int
}, total=False)
ProfessionInfo = TypedDict("ProfessionInfo", {
    "level": int,
    "xpPercent": int
})
ProfessionsData = TypedDict("ProfessionsData", {
    "fishing": ProfessionInfo,
    "woodcutting": ProfessionInfo,
    "mining": ProfessionInfo,
    "farming": ProfessionInfo,
    "scribing": ProfessionInfo,
    "jeweling": ProfessionInfo,
    "alchemism": ProfessionInfo,
    "cooking": ProfessionInfo,
    "weaponsmithing": ProfessionInfo,
    "tailoring": ProfessionInfo,
    "woodworking": ProfessionInfo,
    "armouring": ProfessionInfo
})
CharacterInfo = TypedDict("CharacterInfo", {
    "type": str,
    "nickname": str,
    "level": int,
    "xp": int,
    "xpPercent": int,

    "totalLevel": int,
    "wars": int,
    "playtime": float,
    "mobsKilled": int,
    "chestsFound": int,
    "blocksWalked": int,
    "itemsIdentified": int,
    "logins": int,
    "deaths": int,
    "discoveries": int,

    "pvp": PvpInfo,
    "skillPoints": SkillPointsInfo,
    "professions": Union[ProfessionsData, Dict[str, ProfessionInfo]],  # TODO: INCOMPLETE

    "preEconomy": bool,
    "gamemode": List[str],  # TODO: INCOMPLETE
    "dungeons": DungeonInfo,
    "raids": RaidInfo,
    "quests": List[str]  # TODO: INCOMPLETE
})
GlobalData = TypedDict("GlobalData", {
    "wars": int,
    "totalLevels": int,
    "killedMobs": int,
    "chestsFound": int,
    "dungeons": DungeonInfo,
    "raids": RaidInfo,
    "completedQuests": int,
    "pvp": PvpInfo
})
ForumLinkInfo = TypedDict("ForumLinkInfo", {
    "forumUsername": str,
    "forumId": int,
    "gameUsername": str
})
RankingInfo = TypedDict("RankingInfo", {})  # TODO: INCOMPLETE
PlayerStats = TypedDict("PlayerStats", {
    "username": str,
    "online": bool,
    "server": str,
    "uuid": str,
    "rank": str,
    "rankBadge": str,
    "legacyRankColour": Dict[str, str],  # TODO: INCOMPLETE
    "shortenedRank": str,
    "supportRank": Optional[str],  # TODO: INCOMPLETE
    "firstJoin": str,
    "lastJoin": str,
    "playtime": float,
    "guild": GuildInfo,
    "global_data": GlobalData,
    "forumLink": ForumLinkInfo,
    "ranking": Dict[str, int],  # TODO: INCOMPLETE
    "characters": Dict[str, CharacterInfo],
    "publicProfile": bool
})

FetchedPlayer = TypedDict("FetchedPlayer", {"response_timestamp": float, "player_stats": "PlayerStats"})
FetchedGuild = TypedDict("FetchedGuild", {"response_timestamp": float, "guild_stats": "GuildStats"})

lFetchedPlayers: TypeAlias = List[FetchedPlayer]
lFetchedGuilds: TypeAlias = List[FetchedGuild]
