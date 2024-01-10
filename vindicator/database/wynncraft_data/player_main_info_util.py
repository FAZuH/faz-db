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


class PlayerMainInfoUtil:

    def __init__(self, fetched_players: List[FetchedPlayer]) -> None:
        self._to_insert: List[PlayerMainInfoDB_I] = []
        for fetched_player in fetched_players:
            player_stats: PlayerStats = fetched_player["player_stats"]
            try:
                player: PlayerMainInfoDB_I = {
                    "first_join": WynncraftResponseUtil.iso_to_sqldt(player_stats["firstJoin"]),
                    "latest_username": player_stats["username"],
                    "uuid": WynncraftResponseUtil.format_uuid(player_stats["uuid"]),
                }
                self._to_insert.append(player)
            except Exception as e:
                try:
                    error_message: dict = {
                        "error": str(e),
                        "data recipient": PLAYER_MAIN_INFO,
                        "username": player_stats["username"],
                        "timestamp": f"<t:{int(time())}>",
                    }
                except Exception as e:
                    error_message: dict = {"error": str(e), "message": "Failed building error message."}
                create_task(VindicatorWebhook.log("error", "error", error_message, title="Wynn response parsing"))
                continue

    async def to_db(self) -> None:
        query = (
           f"INSERT INTO {PLAYER_MAIN_INFO} "
           "(first_join, latest_username, uuid) "
           "VALUES (%(first_join)s, %(latest_username)s, %(uuid)s) "
           "ON DUPLICATE KEY UPDATE "
           "latest_username = CASE "
           "    WHEN VALUES(latest_username) <> latest_username THEN VALUES(latest_username) "
           "    ELSE latest_username "
           "END"
        )
        await WynncraftDataDatabase.execute(query, self._to_insert)
