from typing import Optional, TypedDict


__version__: str = "0.0.1"
API_KEY: Optional[str] = None

FETCH_GUILD_INTERVAL: int = 600
FETCH_ONLINE_INTERVAL: int = 30
FETCH_PLAYER_INTERVAL: int = 30


class DatabaseTables:
    GUILD_MAIN = "guild_main"
    GUILD_MAIN_INFO = "guild_main_info"
    GUILD_MEMBER = "guild_member"
    PLAYER_ACTIVITY = "player_activity"
    PLAYER_CHARACTER = "player_character"
    PLAYER_CHARACTER_INFO = "player_character_info"
    PLAYER_MAIN = "player_main"
    PLAYER_MAIN_INFO = "player_main_info"
    RAW_RESPONSES = "raw_responses"

class Webhooks:
    FETCH_GUILD_WEBHOOK: str = "https://discord.com/api/webhooks/1165646068659265657/J1-COoyU3l-ez4q0d3BG_wb-MoD7GOXWeyWXs6Qy_SqHKF9ecqrDGDZpGLlsO2H_G75S"
    FETCH_ONLINE_WEBHOOK: str = "https://discord.com/api/webhooks/1175279388670042162/ymcM1IbmcEVKLgznxBLVRfbiGQqnw18hvyM14VzV_FGA3QdJPE-Y9N6Twqrqmcj_nGtK"
    FETCH_PLAYER_WEBHOOK: str = "https://discord.com/api/webhooks/1165645953462706266/AoIOMYmY9pdP8kCWqNFjjBZjCPGmVVeuSqoOjexi2mKbNSCBubGw5nRcP_EiARxWBK-T"
    DATABASE_WEBHOOK: str = "https://discord.com/api/webhooks/1175107043649138799/rsGUi3EQ1p8FBYA9o59KrZ9NEGN8hFxy9Yx9X9kNrTGbKxD86XvRYp7wWcJ0hUkirxIp"
    ERROR_WEBHOOK: str = "https://discord.com/api/webhooks/1175107206136463480/r9P468IHTLYzDcdCd6jM4pAYjb-sDqCAY38davwv8HehRrBZ2fRplb4JeCzYqf7U6WMV"

CacheInfo = TypedDict("CacheInfo", {
    "ttl": int
})
CacheSettings = TypedDict("CacheSettings", {
    "online_player_list": CacheInfo,
    "guild_stats": CacheInfo,
    "player_stats": CacheInfo,
    "guild_list": CacheInfo,
})

CACHE_SETTINGS: CacheSettings = {
    "online_player_list": {
        "ttl": 300
    },
    "guild_stats": {
        "ttl": 259_200
    },
    "player_stats": {
        "ttl": 259_200
    },
    "guild_list": {
        "ttl": 10_800
    }
}
