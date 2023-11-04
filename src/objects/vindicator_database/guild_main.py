from dataclasses import dataclass, asdict
from typing import TYPE_CHECKING, List

from database.vindicator_database import VindicatorDatabase
from settings import VindicatorTables
from utils.wynncraft_response_utils import WynncraftResponseUtils as WynnUtils

if TYPE_CHECKING:
    from objects.wynncraft_response import GuildStats
    from request.fetch_guild import FetchedGuild


@dataclass
class GuildMain:
    level: float  # NOTE: decimal(5, 2)
    member_total: int  # NOTE: tinyint unsigned
    name: str  # NOTE: varchar(30)
    online_members: int  # NOTE: tinyint unsigned
    territories: int  # NOTE: smallint unsigned
    unique_hash: bytes  # NOTE: binary(32)
    wars: int  # NOTE: int unsigned

    @classmethod
    def from_raw(cls, fetched_guilds: List["FetchedGuild"]) -> List[dict]:
        ret = []

        for fetched_guild in fetched_guilds:

            guild_stats: "GuildStats" = fetched_guild["guild_stats"]

            guild: GuildMain = cls(**{key: None for key in cls.__annotations__})  # type: ignore

            guild.level = float(guild_stats["level"] + (guild_stats["xpPercent"] / 100))
            guild.member_total = guild_stats["members"]["total"]
            guild.name = guild_stats["name"]
            guild.online_members = guild_stats["online"]
            guild.territories = guild_stats["territories"]
            guild.wars = guild_stats["wars"]
            guild.unique_hash = WynnUtils.compute_hash(
                ''.join(
                    [str(value) for value in asdict(guild).values() if value]
                )
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

