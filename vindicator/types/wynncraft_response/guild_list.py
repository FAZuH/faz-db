from typing import List, TypeAlias, TypedDict


GuildRecord = TypedDict("GuildRecord", {
    "name": str,
    "prefix": str
})
GuildList: TypeAlias = List[GuildRecord]
