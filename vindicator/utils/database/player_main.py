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


class PlayerMain:

    @classmethod
    def from_raw(cls, fetched_players: lFetchedPlayers) -> List[PlayerMainT]:
        ret: List[PlayerMainT] = []
        for fetched_player in fetched_players:
            player_stats: PlayerStats = fetched_player["player_stats"]
            try:
                player_main: PlayerMainT = {
                    "guild_name" : player_stats["guild"]["name"] if player_stats["guild"] else None,
                    "guild_rank" : player_stats["guild"]["rank"].upper() if player_stats["guild"] else None,
                    "playtime" : player_stats["playtime"],
                    "support_rank" : player_stats["supportRank"],
                    "rank": player_stats["rank"],
                    "username" : player_stats["username"],
                    "uuid" : WynncraftResponseUtils.format_uuid(player_stats["uuid"])
                }
                player_main["unique_hash"] = WynncraftResponseUtils.compute_hash(''.join([str(value) for value in player_main.values() if value]))
                player_main["timestamp"] = int(fetched_player["response_timestamp"])
                ret.append(player_main)
            except Exception as e:
                try:
                    error_message = {
                        "error": str(e),
                        "data recipient": PLAYER_CHARACTER,
                        "username": player_stats["username"],
                        "timestamp": f"<t:{int(time())}>",
                    }
                except Exception as e:
                    error_message: dict = {"error": str(e), "message": "Failed building error message."}
                create_task(VindicatorWebhook.log("error", "error", error_message, title="Wynn response parsing"))
                continue
        return ret

    @classmethod
    async def to_db(cls, fetched_players: lFetchedPlayers) -> None:
        params: List[PlayerMainT] = PlayerMain.from_raw(fetched_players)
        query = (
            f"INSERT INTO {PLAYER_MAIN} "
            "(guild_name, guild_rank, playtime, support_rank, `rank`, timestamp, unique_hash, username, uuid) "
            "VALUES "
            "(%(guild_name)s, %(guild_rank)s, %(playtime)s, %(support_rank)s, %(rank)s, %(timestamp)s, %(unique_hash)s, %(username)s, %(uuid)s) "
            "ON DUPLICATE KEY UPDATE "
            "timestamp = VALUES(timestamp)"
        )
        await WynncraftDataDatabase.write_many(query, params)  # type: ignore
