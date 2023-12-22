from typing import TypedDict


GuildMemberT = TypedDict("GuildMember", {
    "joined": int,  # int unsigned
    "uuid": bytes,  # binary(16)
    "contributed": int,  # bigint unsigned

    "unique_hash": bytes,  # binary(32)
    "timestamp": int,  # int unsigned
})
