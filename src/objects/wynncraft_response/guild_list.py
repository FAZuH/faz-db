from typing import List, TypedDict


GuildList = List[
    TypedDict("GuildRecord", {
            "name": str,
            "prefix": str
    })
]
