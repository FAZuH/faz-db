from typing import TypedDict


class GuildMain(TypedDict):
    level: float  # NOTE: decimal(5, 2)
    member_total: int  # NOTE: tinyint unsigned
    name: str  # NOTE: varchar(30)
    online_members: int  # NOTE: tinyint unsigned
    territories: int  # NOTE: smallint unsigned
    unique_hash: bytes  # NOTE: binary(32)
    wars: int  # NOTE: int unsigned
