from __future__ import annotations
from typing import TYPE_CHECKING, List, TypedDict

from database.vindicator_database import VindicatorDatabase
from constants import DatabaseTables
from utils.wynncraft_response_utils import WynncraftResponseUtils as WynnUtils

if TYPE_CHECKING:
    from objects.wynncraft_response import GuildStats
    from request.fetch_guild import FetchedGuild


class GuildMain:
    TYPE = TypedDict("GuildMain", {
        "level": float,  # decimal(5, 2)
        "member_total": int,  # tinyint unsigned
        "name": str,  # varchar(30)
        "online_members": int,  # tinyint unsigned
        "territories": int,  # smallint unsigned
        "wars": int,  # int unsigned

        "unique_hash": bytes,  # binary(32)
        "timestamp": int,  # int unsigned
    })

    @staticmethod
    def from_raw(fetched_guilds: List["FetchedGuild"]) -> List[GuildMain.TYPE]:
        ret: List[GuildMain.TYPE] = []

        for fetched_guild in fetched_guilds:
            guild_stats: "GuildStats" = fetched_guild["guild_stats"]
            guild_main: GuildMain.TYPE = {  # type: ignore
                "level": float(guild_stats["level"] + (guild_stats["xpPercent"] / 100)),
                "member_total": guild_stats["members"]["total"],
                "name": guild_stats["name"],
                "online_members": guild_stats["online"],
                "territories": guild_stats["territories"],
                "wars": guild_stats["wars"],
            }
            guild_main["unique_hash"] = WynnUtils.compute_hash(''.join([str(value) for value in guild_main.values() if value]))
            guild_main["timestamp"] = int(fetched_guild["response_timestamp"])
            ret.append(guild_main)

        return ret

    @staticmethod
    async def to_db(guild_main: List[dict]) -> None:
        query: str = (
            f"INSERT IGNORE INTO {DatabaseTables.GUILD_MAIN} (level, member_total, name, online_members, territories, unique_hash, wars) "
            "VALUES (%(level)s, %(member_total)s, %(name)s, %(online_members)s, %(territories)s, %(unique_hash)s, %(wars)s)"
        )
        await VindicatorDatabase.write_many(query, guild_main)

