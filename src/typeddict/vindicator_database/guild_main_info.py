from typing import TypedDict


class GuildMainInfo:
    created: int  # NOTE: int unsigned
    name: str  # NOTE: varchar(30)
    prefix: str  # NOTE: varchar(4)
