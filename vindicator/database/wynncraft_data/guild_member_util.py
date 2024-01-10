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


class GuildMemberUtil:

    def __init__(self, fetched_guilds: List[FetchedGuild]) -> None:
        self._to_insert: List[GuildMemberDB_I] = []
        for fetched_guild in fetched_guilds:
            guild_stats: GuildStats = fetched_guild["guild_stats"]
            try:
                for rank, guild_members in guild_stats["members"].items():
                    if rank == "total":
                        continue
                    for guild_member_info in guild_members.values():  # type: ignore
                        guild_member_info: GuildMemberInfo
                        guild_member: GuildMemberDB_I = {  # type: ignore
                            "joined": WynncraftResponseUtil.iso_to_sqldt(guild_member_info["joined"]),
                            "uuid": WynncraftResponseUtil.format_uuid(guild_member_info["uuid"]),
                            "contributed": int(guild_member_info["contributed"]),
                        }
                        guild_member["unique_hash"] = WynncraftResponseUtil.compute_hash(''.join([str(value) for value in guild_member.values() if value]))
                        guild_member["datetime"] = fetched_guild["resp_datetime"]
                        self._to_insert.append(guild_member)
            except Exception as e:
                try:
                    error_message = {
                        "error": str(e),
                        "data recipient": GUILD_MEMBER,
                        "username": guild_stats["name"],
                        "timestamp": f"<t:{int(time())}>",
                    }
                except Exception as e:
                    error_message: dict = {"error": str(e), "message": "Failed building error message."}
                create_task(VindicatorWebhook.log("error", "error", error_message, title="Wynn response parsing"))
                continue

    async def to_db(self) -> None:
        query: str = (
            f"INSERT IGNORE INTO {GUILD_MEMBER} (joined, uuid, contributed, datetime, unique_hash) "
            "VALUES (%(joined)s, %(uuid)s, %(contributed)s, %(datetime)s, %(unique_hash)s)"
        )
        await WynncraftDataDatabase.execute(query, self._to_insert)
