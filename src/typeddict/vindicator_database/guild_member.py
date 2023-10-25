from typing import TypedDict


class GuildMember(TypedDict):
    joined: int  # NOTE: int unsigned
    uuid: bytes  # NOTE: binary(16)
    xp_contributed: int  # NOTE: bigint unsigned
