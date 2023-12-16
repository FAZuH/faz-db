from __future__ import annotations
from typing import TYPE_CHECKING, List, TypedDict

from constants import DatabaseTables
from database.vindicator_database import VindicatorDatabase
from utils.wynncraft_response_utils import WynncraftResponseUtils as WynnUtils

if TYPE_CHECKING:
    from objects.wynncraft_response import GuildStats
    from request.fetch_guild import FetchedGuild


class GuildMainInfo:
    TYPE = TypedDict("GuildMainInfo", {
        "created": int,  # int unsigned
        "name": str,  # varchar(30)
        "prefix": str  # varchar(4)
    })

    @staticmethod
    def from_raw(fetched_guilds: List["FetchedGuild"]) -> List[GuildMainInfo.TYPE]:
        ret: List[GuildMainInfo.TYPE] = []

        for fetched_guild in fetched_guilds:
            guild_stats: "GuildStats" = fetched_guild["guild_stats"]
            ret.append({
                "created": int(WynnUtils.parse_datestr2(guild_stats["created"])),
                "name": guild_stats["name"],
                "prefix": guild_stats["prefix"],
            })

        return ret

    @staticmethod
    async def to_db(guild_main_info: List[dict]) -> None:
        query: str = (  # NOTE: This doesn't change. Ignore duplicates.
            f"INSERT IGNORE INTO {DatabaseTables.GUILD_MAIN_INFO} (created, name, prefix) "
            "VALUES (%(created)s, %(name)s, %(prefix)s)"
        )
        await VindicatorDatabase.write_many(query, guild_main_info)
