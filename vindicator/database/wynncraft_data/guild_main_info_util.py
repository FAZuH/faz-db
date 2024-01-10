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


class GuildMainInfoUtil:

    def __init__(self, fetched_guilds: List[FetchedGuild]) -> None:
        self._to_insert: List[GuildMainInfoDB_I] = []
        for fetched_guild in fetched_guilds:
            guild_stats: "GuildStats" = fetched_guild["guild_stats"]
            try:
                self._to_insert.append({
                    "created": WynncraftResponseUtil.iso_to_sqldt(guild_stats["created"]),
                    "name": guild_stats["name"],
                    "prefix": guild_stats["prefix"],
                })
            except Exception as e:
                try:
                    error_message = {
                        "error": str(e),
                        "data recipient": GUILD_MAIN_INFO,
                        "username": guild_stats["name"],
                        "timestamp": f"<t:{int(time())}>",
                    }
                except Exception as e:
                    error_message: dict = {"error": str(e), "message": "Failed building error message."}
                create_task(VindicatorWebhook.log("error", "error", error_message, title="Wynn response parsing"))
                continue

    async def to_db(self) -> None:
        query: str = (
            # NOTE: This doesn't change. Ignore duplicates.
            f"INSERT IGNORE INTO {GUILD_MAIN_INFO} (created, name, prefix) "
            "VALUES (%(created)s, %(name)s, %(prefix)s)"
        )
        await WynncraftDataDatabase.execute(query, self._to_insert)
