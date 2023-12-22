from typing import TypedDict


GuildMainT = TypedDict("GuildMain", {
    "level": float,  # decimal(5, 2)
    "member_total": int,  # tinyint unsigned
    "name": str,  # varchar(30)
    "online_members": int,  # tinyint unsigned
    "territories": int,  # smallint unsigned
    "wars": int,  # int unsigned

    "unique_hash": bytes,  # binary(32)
    "timestamp": int,  # int unsigned
})
