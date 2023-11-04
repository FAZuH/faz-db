from typing import Dict, List, Optional, TypedDict, Union


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
    "playtime": int,
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
    "playtime": int,
    "guild": GuildInfo,
    "global_data": GlobalData,
    "forumLink": ForumLinkInfo,
    "ranking": Dict[str, int],  # TODO: INCOMPLETE
    "characters": Dict[str, CharacterInfo],
    "publicProfile": bool
})
