from typing import Optional

# MySQL
MYSQL_DT_FMT: str = "%Y-%m-%d %H:%M:%S"

# Vindicator
__version__: str = "0.0.1"
API_KEY: Optional[str] = None

# Fetchers
FETCH_GUILD_INTERVAL: int = 30
FETCH_ONLINE_INTERVAL: int = 30
FETCH_PLAYER_INTERVAL: int = 30

# Discord IDs
DEVELOPER_DISCORD_ID: int = 257428751560867840

# Wynncraft Data Database Tables
GUILD_MAIN: str = "guild_main"
GUILD_MAIN_INFO: str = "guild_main_info"
GUILD_MEMBER: str = "guild_member"
PLAYER_ACTIVITY: str = "player_activity"
PLAYER_CHARACTER: str = "player_character"
PLAYER_CHARACTER_INFO: str = "player_character_info"
PLAYER_MAIN: str = "player_main"
PLAYER_MAIN_INFO: str = "player_main_info"
PLAYER_SERVER: str = "player_server"
CACHE: str = "cache"

# Webhook links
DATABASE_WEBHOOK: str = "https://discord.com/api/webhooks/1175107043649138799/rsGUi3EQ1p8FBYA9o59KrZ9NEGN8hFxy9Yx9X9kNrTGbKxD86XvRYp7wWcJ0hUkirxIp"
ERROR_WEBHOOK: str = "https://discord.com/api/webhooks/1175107206136463480/r9P468IHTLYzDcdCd6jM4pAYjb-sDqCAY38davwv8HehRrBZ2fRplb4JeCzYqf7U6WMV"
FETCH_GUILD_WEBHOOK: str = "https://discord.com/api/webhooks/1165646068659265657/J1-COoyU3l-ez4q0d3BG_wb-MoD7GOXWeyWXs6Qy_SqHKF9ecqrDGDZpGLlsO2H_G75S"
FETCH_ONLINE_WEBHOOK: str = "https://discord.com/api/webhooks/1175279388670042162/ymcM1IbmcEVKLgznxBLVRfbiGQqnw18hvyM14VzV_FGA3QdJPE-Y9N6Twqrqmcj_nGtK"
FETCH_PLAYER_WEBHOOK: str = "https://discord.com/api/webhooks/1165645953462706266/AoIOMYmY9pdP8kCWqNFjjBZjCPGmVVeuSqoOjexi2mKbNSCBubGw5nRcP_EiARxWBK-T"
WYNNCRAFT_REQUEST_WEBHOOK: str = "https://discord.com/api/webhooks/1185935055453945918/X0cgZ9H6jSm5tDbS1w1XXJ7s7xJD2e7Ng7ZqWQUJuIK-2oTRxoyQfFxuPK2eoYxbNC4O"
