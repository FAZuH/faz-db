from __future__ import annotations
from asyncio import create_task
from time import time
from typing import TYPE_CHECKING, List

from vindicator import (
    WynncraftDataDatabase,
    VindicatorWebhook,
    WynncraftResponseUtils
)
from vindicator.constants import *

if TYPE_CHECKING:
    from vindicator.types import *


class GuildMain:

    @classmethod
    def from_raw(cls, fetched_guilds: lFetchedGuilds) -> List[GuildMainT]:
        ret: List[GuildMainT] = []
        for fetched_guild in fetched_guilds:
            guild_stats: "GuildStats" = fetched_guild["guild_stats"]
            try:
                guild_main: GuildMainT = {  # type: ignore
                    "level": float(guild_stats["level"] + (guild_stats["xpPercent"] / 100)),
                    "member_total": guild_stats["members"]["total"],
                    "name": guild_stats["name"],
                    "online_members": guild_stats["online"],
                    "territories": guild_stats["territories"],
                    "wars": guild_stats["wars"],
                }
                guild_main["unique_hash"] = WynncraftResponseUtils.compute_hash(''.join([str(value) for value in guild_main.values() if value]))
                guild_main["timestamp"] = int(fetched_guild["response_timestamp"])
                ret.append(guild_main)
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
        return ret

    @classmethod
    async def to_db(cls, fetched_guilds: lFetchedGuilds) -> None:
        params: List[GuildMainT] = cls.from_raw(fetched_guilds)
        query: str = (
            f"INSERT IGNORE INTO {GUILD_MAIN} (level, member_total, name, online_members, territories, unique_hash, wars) "
            "VALUES (%(level)s, %(member_total)s, %(name)s, %(online_members)s, %(territories)s, %(unique_hash)s, %(wars)s)"
        )
        await WynncraftDataDatabase.write_many(query, params)  # type: ignore

