from dataclasses import dataclass, asdict
from typing import TYPE_CHECKING, List

from database.vindicator_database import VindicatorDatabase
from settings import VindicatorTables
from utils.wynncraft_response_utils import WynncraftResponseUtils as WynnUtils

if TYPE_CHECKING:
    from objects.wynncraft_response.guild_stats import GuildStats, GuildMembers, GuildMemberInfo
    from request.fetch_guild import FetchedGuild


@dataclass
class GuildMember:
    joined: int  # NOTE: int unsigned
    uuid: bytes  # NOTE: binary(16)
    xp_contributed: int  # NOTE: bigint unsigned

    @classmethod
    def from_raw(cls, fetched_guilds: List["FetchedGuild"]) -> List[dict]:
        ret = []

        for fetched_guild in fetched_guilds:

            guild_stats: "GuildStats" = fetched_guild["guild_stats"]
            guild_members: List["GuildMember"] = [*members for rank, members in guild_stats["members"].items() if rank != "total"]  # type: ignore

            for guild_member in guild_members:
                guild_member[]
                guild = cls(
                    joined=int(WynnUtils.parse_datestr2(guild_member[]))
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

