from typing import TypedDict


class PlayerMain(TypedDict):
    guild_name: str  # NOTE: varchar(30)
    guild_rank: str  # NOTE: enum('OWNER', 'CHIEF', 'STRATEGIST', 'CAPTAIN', 'RECRUITER', 'RECRUIT)
    playtime: int  # NOTE: int unsigned
    support_rank: str  # NOTE: varchar(45)
    timestamp: int  # NOTE: int unsigned
    unique_hash: bytes  # NOTE: binary(32)
    username: str  # NOTE: varchar(16)
    uuid: bytes  # NOTE: binary(16)
