from typing import TypedDict


PlayerCharacterInfoT = TypedDict("PlayerCharacterInfo", {
    "character_uuid": bytes,  # binary(16)
    "type": str,  # enum('ARCHER', 'ASSASSIN', 'MAGE', 'SHAMAN', 'WARRIOR')
    "uuid": bytes  # binary(16)
})
