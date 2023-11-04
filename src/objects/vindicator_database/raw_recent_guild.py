from typing import TypedDict, Union


class RawRecentGuild(TypedDict):
    guild_name: str  # NOTE: varchar(30)
    response: Union[dict, list]  # NOTE: json
    timestamp: int  # NOTE: int unsigned

from dataclasses import dataclass, asdict
from typing import TYPE_CHECKING, List

from database.vindicator_database import VindicatorDatabase
from settings import VindicatorTables
from utils.wynncraft_response_utils import WynncraftResponseUtils as WynnUtils

if TYPE_CHECKING:
    from objects.wynncraft_response import GuildStats
    from request.fetch_guild import FetchedGuild


@dataclass
class GuildMainInfo:
    created: int  # NOTE: int unsigned
    name: str  # NOTE: varchar(30)
    prefix: str  # NOTE: varchar(4)

    @classmethod
    def from_raw(cls, fetched_guilds: List["FetchedGuild"]) -> List[dict]:
        ret = []

        for fetched_guild in fetched_guilds:

            guild_stats: "GuildStats" = fetched_guild["guild_stats"]

            guild = cls(
                created=int(WynnUtils.parse_datestr2(guild_stats["created"])),
                name=guild_stats["name"],
                prefix=guild_stats["prefix"],
            )
            ret.append(asdict(guild))

        return ret

    @staticmethod
    async def to_db(guild_main_info: List[dict]) -> None:
        query: str = (
            "INSERT IGNORE INTO guild_main_info (created, name, prefix) "
            "VALUES (%(created)s, %(name)s, %(prefix)s)"
        )
        await VindicatorDatabase.write_many(query, guild_main_info)

