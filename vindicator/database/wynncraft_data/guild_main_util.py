from __future__ import annotations
from asyncio import create_task
from time import time

from vindicator import (
    WynncraftDataDatabase,
    VindicatorWebhook,
    WynncraftResponseUtil
)
from vindicator.constants import *
from vindicator.typehints import *


class GuildMainUtil:

    def __init__(self, fetched_guilds: List[FetchedGuild]) -> None:
        self._to_insert: List[GuildMainDB_I] = []
        for fetched_guild in fetched_guilds:
            guild_stats: "GuildStats" = fetched_guild["guild_stats"]
            try:
                guild_main: GuildMainDB_I = {  # type: ignore
                    "level": float(guild_stats["level"] + (guild_stats["xpPercent"] / 100)),
                    "member_total": guild_stats["members"]["total"],
                    "name": guild_stats["name"],
                    "online_members": guild_stats["online"],
                    "territories": guild_stats["territories"],
                    "wars": guild_stats["wars"],
                }
                guild_main["unique_hash"] = WynncraftResponseUtil.compute_hash(''.join([str(value) for value in guild_main.values() if value]))
                guild_main["datetime"] = fetched_guild["resp_datetime"]
                self._to_insert.append(guild_main)
            except Exception as e:
                try:
                    error_message = {
                        "error": str(e),
                        "data recipient": PLAYER_CHARACTER,
                        "username": guild_stats["name"],
                        "timestamp": f"<t:{int(time())}>",
                    }
                except Exception as e:
                    error_message: dict = {"error": str(e), "message": "Failed building error message."}
                create_task(VindicatorWebhook.log("error", "error", error_message, title="Wynn response parsing"))
                continue

    async def to_db(self) -> None:
        query: str = (
            f"INSERT IGNORE INTO {GUILD_MAIN} (level, member_total, name, online_members, territories, unique_hash, wars, datetime) "
            "VALUES (%(level)s, %(member_total)s, %(name)s, %(online_members)s, %(territories)s, %(unique_hash)s, %(wars)s, %(datetime)s)"
        )
        await WynncraftDataDatabase.execute(query, self._to_insert)

