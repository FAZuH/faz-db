from typing import TypedDict


PlayerCharacterT = TypedDict(("PlayerCharacter"), {
    "character_uuid": bytes,  # binary(16)

    # Professions
    "alchemism": float,  # decimal(5, 2) unsigned
    "armouring": float,  # decimal(5, 2) unsigned
    "cooking": float,  # decimal(5, 2) unsigned
    "farming": float,  # decimal(5, 2) unsigned
    "fishing": float,  # decimal(5, 2) unsigned
    "jeweling": float,  # decimal(5, 2) unsigned
    "mining": float,  # decimal(5, 2) unsigned
    "scribing": float,  # decimal(5, 2) unsigned
    "tailoring": float,  # decimal(5, 2) unsigned
    "weaponsmithing": float,  # decimal(5, 2) unsigned
    "woodcutting": float,  # decimal(5, 2) unsigned
    "woodworking": float,  # decimal(5, 2) unsigned

    # Direct
    "chests_found": int,  # int unsigned
    "deaths": int,  # int unsigned
    "discoveries": int,  # int unsigned
    "level": float,  # decimal(5, 2) unsigned
    "logins": int,  # int unsigned
    "mobs_killed": int,  # int unsigned
    "playtime": int,  # int unsigned
    "wars": int,  # int unsigned
    "xp": int,  # bigint unsigned
    "dungeon_completions": int,  # int unsigned
    "quest_completions": int,  # int unsigned
    "raid_completions": int,  # int unsigned

    # Needs special computation
    "gamemode": bytes,  # bit(5)

    "unique_hash": bytes,  # binary(32)
    "timestamp": int,  # int unsigned
})
