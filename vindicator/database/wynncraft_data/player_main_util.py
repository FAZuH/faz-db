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


class PlayerMainUtil:

    def __init__(self, fetched_players: List[FetchedPlayer]) -> None:
        self._to_insert: List[PlayerMainDB_I] = []
        for fetched_player in fetched_players:
            player_stats: PlayerStats = fetched_player["player_stats"]
            try:
                player_main: PlayerMainDB_I = {
                    "guild_name" : player_stats["guild"]["name"] if player_stats["guild"] else None,
                    "guild_rank" : player_stats["guild"]["rank"].upper() if player_stats["guild"] else None,
                    "playtime" : player_stats["playtime"],
                    "support_rank" : player_stats["supportRank"],
                    "rank": player_stats["rank"],
                    "username" : player_stats["username"],
                    "uuid" : WynncraftResponseUtil.format_uuid(player_stats["uuid"])
                }
                player_main["unique_hash"] = WynncraftResponseUtil.compute_hash(''.join([str(value) for value in player_main.values() if value]))
                player_main["datetime"] = fetched_player["resp_datetime"]
                self._to_insert.append(player_main)
            except Exception as e:
                try:
                    error_message = {
                        "error": str(e),
                        "data recipient": PLAYER_MAIN,
                        "username": player_stats["username"],
                        "timestamp": f"<t:{int(time())}>",
                    }
                except Exception as e:
                    error_message: dict = {"error": str(e), "message": "Failed building error message."}
                create_task(VindicatorWebhook.log("error", "error", error_message, title="Wynn response parsing"))
                continue

    async def to_db(self) -> None:
        query = (
            f"INSERT INTO {PLAYER_MAIN} "
            "(guild_name, guild_rank, playtime, support_rank, `rank`, datetime, unique_hash, username, uuid) "
            "VALUES "
            "(%(guild_name)s, %(guild_rank)s, %(playtime)s, %(support_rank)s, %(rank)s, %(datetime)s, %(unique_hash)s, %(username)s, %(uuid)s) "
            "ON DUPLICATE KEY UPDATE "
            "datetime = VALUES(datetime)"
        )
        await WynncraftDataDatabase.execute(query, self._to_insert)
