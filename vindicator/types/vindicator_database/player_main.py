from typing import Optional, TypedDict


PlayerMainT = TypedDict("PlayerMain", {
    "guild_name": Optional[str],  # varchar(30)
    "guild_rank": Optional[str],  # enum('OWNER', 'CHIEF', 'STRATEGIST', 'CAPTAIN', 'RECRUITER', 'RECRUIT)
    "playtime": int,  # int unsigned
    "support_rank": Optional[str],  # varchar(45)
    "username": str,  # varchar(16)
    "uuid": bytes,  # binary(16)

    "unique_hash": bytes,  # binary(32)
    "timestamp": int,  # int unsigned
}, total=False)
