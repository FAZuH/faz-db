from __future__ import annotations
from asyncio import create_task
from time import time
from typing import TYPE_CHECKING, List

from vindicator import (
    DatabaseTables,
    WynncraftDataDatabase,
    VindicatorWebhook,
    WynncraftResponseUtils
)

if TYPE_CHECKING:
    from vindicator.types import *


class GuildMainInfo:

    @classmethod
    def from_raw(cls, fetched_guilds: lFetchedGuilds) -> List[GuildMainInfoT]:
        ret: List[GuildMainInfoT] = []
        for fetched_guild in fetched_guilds:
            guild_stats: "GuildStats" = fetched_guild["guild_stats"]
            try:
                ret.append({
                    "created": int(WynncraftResponseUtils.parse_datestr2(guild_stats["created"])),
                    "name": guild_stats["name"],
                    "prefix": guild_stats["prefix"],
                })
            except Exception as e:
                try:
                    error_message = {
                        "error": str(e),
                        "data recipient": DatabaseTables.PLAYER_CHARACTER,
                        "username": guild_stats["name"],
                        "timestamp": f"<t:{int(time())}>",
                    }
                except Exception as e:
                    error_message: dict = {"error": str(e), "message": "Failed building error message."}
                create_task(VindicatorWebhook.log("error", "error", error_message, title="Wynn response parsing"))
                continue
        return ret

    @classmethod
    async def to_db(cls, fetched_guilds: lFetchedGuilds) -> None:
        params: List[GuildMainInfoT] = cls.from_raw(fetched_guilds)
        query: str = (  # NOTE: This doesn't change. Ignore duplicates.
            f"INSERT IGNORE INTO {DatabaseTables.GUILD_MAIN_INFO} (created, name, prefix) "
            "VALUES (%(created)s, %(name)s, %(prefix)s)"
        )
        await WynncraftDataDatabase.write_many(query, params)  # type: ignore
