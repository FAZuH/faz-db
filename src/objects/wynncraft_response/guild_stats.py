from typing import Dict, List, Optional, TypedDict


Username = Rank = str

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
    "owner": Dict[Username, GuildMember],
    "chief": Dict[Username, GuildMember],
    "strategist": Dict[Username, GuildMember],
    "captain": Dict[Username, GuildMember],
    "recruiter": Dict[Username, GuildMember],
    "recruit": Dict[Username, GuildMember]
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
