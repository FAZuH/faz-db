from typing import TypedDict


class PlayerCharacter(TypedDict):
    alchemism: float  # NOTE: decimal(5, 2) unsigned
    armouring: float  # NOTE: decimal(5, 2) unsigned
    character_uuid: bytes  # NOTE: binary(16)
    chests_found: int  # NOTE: int unsigned
    cooking: float  # NOTE: decimal(5, 2) unsigned
    deaths: int  # NOTE: int unsigned
    discoveries: int  # NOTE: int unsigned
    dungeon_completions: int  # NOTE: int unsigned
    farming: float  # NOTE: decimal(5, 2) unsigned
    fishing: float  # NOTE: decimal(5, 2) unsigned
    gamemode: bytes  # NOTE: bit(4)
    jeweling: float  # NOTE: decimal(5, 2) unsigned
    level: float  # NOTE: decimal(5, 2) unsigned
    logins: int  # NOTE: int unsigned
    mining: float  # NOTE: decimal(5, 2) unsigned
    mobs_killed: int  # NOTE: int unsigned
    playtime: int  # NOTE: int unsigned
    quest_completions: int  # NOTE: int unsigned
    raid_completions: int  # NOTE: int unsigned
    scribing: float  # NOTE: decimal(5, 2) unsigned
    tailoring: float  # NOTE: decimal(5, 2) unsigned
    timestamp: int  # NOTE: int unsigned
    unique_hash: bytes  # NOTE: binary(32)
    username: str  # NOTE: varchar(16)
    wars: int  # NOTE: int unsigned
    weaponsmithing: float  # NOTE: decimal(5, 2) unsigned
    woodcutting: float  # NOTE: decimal(5, 2) unsigned
    woodworking: float  # NOTE: decimal(5, 2) unsigned
    xp: int  # NOTE: bigint unsigned
