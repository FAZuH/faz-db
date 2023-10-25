from typing import Optional


__version__: str = "0.0.1"
API_KEY: Optional[str] = None

FETCH_GUILD_WEBHOOK: str = "https://discord.com/api/webhooks/1165646068659265657/J1-COoyU3l-ez4q0d3BG_wb-MoD7GOXWeyWXs6Qy_SqHKF9ecqrDGDZpGLlsO2H_G75S"
FETCH_ONLINE_WEBHOOK: str = "https://discord.com/api/webhooks/1165646056361562203/UANq8Dc5KWX_eFhx6QIA39PPaOwoQN1mVGk435Kj7Iy6hgQLOGBZeCNNttnYt7wc6Jnp"
FETCH_PLAYER_WEBHOOK: str = "https://discord.com/api/webhooks/1165645953462706266/AoIOMYmY9pdP8kCWqNFjjBZjCPGmVVeuSqoOjexi2mKbNSCBubGw5nRcP_EiARxWBK-T"

FETCH_GUILD_INTERVAL: int = 600
FETCH_ONLINE_INTERVAL: int = 30
FETCH_PLAYER_INTERVAL: int = 600
\
class VindicatorTables:
    GUILD_MAIN = "guild_main"
    GUILD_MAIN_INFO = "guild_main_info"
    GUILD_MEMBER = "guild_member"
    PLAYER_CHARACTER = "player_character"
    PLAYER_CHARACTER_INFO = "player_character_info"
    PLAYER_MAIN = "player_main"
    PLAYER_MAIN_INFO = "player_main_info"
    PLAYER_UPTIME = "player_uptime"
    RAW_LATEST_GUILD = "raw_latest_guild"
    RAW_LATEST_OTHERS = "raw_latest_others"
    RAW_LATEST_PLAYER = "raw_latest_player"
    RAW_RECENT_GUILD = "raw_recent_guild"
    RAW_RECENT_PLAYER = "raw_recent_player"
