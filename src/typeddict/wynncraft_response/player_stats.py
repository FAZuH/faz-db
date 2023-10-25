from typing import TypedDict, List, Dict, NotRequired


class GuildInfo(TypedDict):
    name: str
    prefix: str
    rank: str
    rankStars: str


# TODO: INCOMPLETE
class DungeonList(TypedDict):
    pass


class DungeonInfo(TypedDict):
    total: int
    list: Dict[str, int]  # TODO: INCOMPLETE


# TODO: INCOMPLETE
class RaidList(TypedDict):
    pass


class RaidInfo(TypedDict):
    total: int
    list: Dict[str, int]  # TODO: INCOMPLETE


class PvpInfo(TypedDict):
    kills: int
    deaths: int


class SkillPointsInfo(TypedDict):
    strength: NotRequired[int]
    dexterity: NotRequired[int]
    intelligence: NotRequired[int]
    defence: NotRequired[int]
    agility: NotRequired[int]


class ProfessionInfo(TypedDict):
    level: int
    xpPercent: int


class ProfessionsData(TypedDict):
    fishing: ProfessionInfo
    woodcutting: ProfessionInfo
    mining: ProfessionInfo
    farming: ProfessionInfo
    scribing: ProfessionInfo
    jeweling: ProfessionInfo
    alchemism: ProfessionInfo
    cooking: ProfessionInfo
    weaponsmithing: ProfessionInfo
    tailoring: ProfessionInfo
    woodworking: ProfessionInfo
    armouring: ProfessionInfo


class CharacterInfo(TypedDict):
    type: str
    nickname: str
    level: int
    xp: int
    xpPercent: int
    totalLevel: int
    wars: int
    playtime: int
    mobsKilled: int
    chestsFound: int
    blocksWalked: int
    itemsIdentified: int
    logins: int
    death: int
    discoveries: int
    pvp: PvpInfo
    gamemode: List[str]
    skillPoints: SkillPointsInfo
    professions: ProfessionsData
    dungeons: DungeonInfo
    raids: RaidInfo
    quests: List[str]


class GlobalData(TypedDict):
    wars: int
    totalLevels: int
    killedMobs: int
    chestsFound: int
    dungeons: DungeonInfo
    raids: RaidInfo
    completedQuests: int
    pvp: PvpInfo


class ForumLinkInfo(TypedDict):
    forumUsername: str
    forumId: int
    gameUsername: str


# TODO: INCOMPLETE
class RankingInfo(TypedDict):
    pass


class PlayerStats(TypedDict):
    username: str
    online: bool
    server: str
    uuid: str
    rank: str
    rankBadge: str
    legacyRankColour: Dict[str, str]
    shortenedRank: str
    supportRank: str
    firstJoin: str
    lastJoin: str
    playtime: int
    guild: GuildInfo
    global_data: GlobalData
    forumLink: ForumLinkInfo
    ranking: Dict[str, int]  # INCOMPLETE
    characters: Dict[str, CharacterInfo]
    publicProfile: bool
