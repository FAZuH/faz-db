from typing import TypedDict


GuildMainInfoT = TypedDict("GuildMainInfo", {
    "created": int,  # int unsigned
    "name": str,  # varchar(30)
    "prefix": str  # varchar(4)
})
