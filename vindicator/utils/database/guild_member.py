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


class GuildMember:

    @classmethod
    def from_raw(cls, fetched_guilds: lFetchedGuilds) -> List[GuildMemberT]:
        ret: List[GuildMemberT] = []
        for fetched_guild in fetched_guilds:
            guild_stats: GuildStats = fetched_guild["guild_stats"]
            try:
                for rank, guild_members in guild_stats["members"].items():
                    if rank == "total":
                        continue
                    for guild_member_info in guild_members.values():  # type: ignore
                        guild_member_info: GuildMemberInfo
                        guild_member: GuildMemberT = {  # type: ignore
                            "joined": int(WynncraftResponseUtils.parse_datestr2(guild_member_info["joined"])),
                            "uuid": WynncraftResponseUtils.format_uuid(guild_member_info["uuid"]),
                            "contributed": int(guild_member_info["contributed"]),
                        }
                        guild_member["unique_hash"] = WynncraftResponseUtils.compute_hash(''.join([str(value) for value in guild_member.values() if value]))
                        guild_member["timestamp"] = int(fetched_guild["response_timestamp"])
                        ret.append(guild_member)
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
        params: List[GuildMemberT] = cls.from_raw(fetched_guilds)
        query: str = (
            f"INSERT IGNORE INTO {DatabaseTables.GUILD_MEMBER} (joined, uuid, contributed, timestamp, unique_hash) "
            "VALUES (%(joined)s, %(uuid)s, %(contributed)s, %(timestamp)s, %(unique_hash)s)"
        )
        await WynncraftDataDatabase.write_many(query, params)  # type: ignore

