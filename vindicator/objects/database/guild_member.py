from __future__ import annotations
from typing import TYPE_CHECKING, List, TypedDict

from database.vindicator_database import VindicatorDatabase
from constants import DatabaseTables
from utils.wynncraft_response_utils import WynncraftResponseUtils as WynnUtils

if TYPE_CHECKING:
    from objects.wynncraft_response.guild_stats import GuildStats, GuildMembers, GuildMemberInfo
    from request.fetch_guild import FetchedGuild


class GuildMember:

    TYPE = TypedDict("GuildMember", {
        "joined": int,  # int unsigned
        "uuid": bytes,  # binary(16)
        "contributed": int,  # bigint unsigned

        "unique_hash": bytes,  # binary(32)
        "timestamp": int,  # int unsigned
    })

    @staticmethod
    def from_raw(fetched_guilds: List["FetchedGuild"]) -> List[GuildMember.TYPE]:
        ret: List[GuildMember.TYPE] = []

        for fetched_guild in fetched_guilds:
            for rank, guild_members in fetched_guild["guild_stats"]["members"].items():
                if rank == "total":
                    continue
                for guild_member_info in guild_members.values():  # type: ignore
                    guild_member: GuildMember.TYPE = {  # type: ignore
                        "joined": int(WynnUtils.parse_datestr2(guild_member_info["joined"])),
                        "uuid": WynnUtils.format_uuid(guild_member_info["uuid"]),
                        "contributed": int(guild_member_info["contributed"]),
                    }
                    guild_member["unique_hash"] = WynnUtils.compute_hash(''.join([str(value) for value in guild_member.values() if value]))
                    guild_member["timestamp"] = int(fetched_guild["response_timestamp"])
                    ret.append(guild_member)

        return ret

    @staticmethod
    async def to_db(guild_member: List[dict]) -> None:
        query: str = (
            f"INSERT IGNORE INTO {DatabaseTables.GUILD_MEMBER} (joined, uuid, contributed) "
            "VALUES (%(joined)s, %(uuid)s, %(contributed)s)"
        )
        await VindicatorDatabase.write_many(query, guild_member)

