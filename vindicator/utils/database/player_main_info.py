from __future__ import annotations
from asyncio import create_task
from time import time
from typing import TYPE_CHECKING, List

from vindicator import (
    ErrorHandler,
    WynncraftDataDatabase,
    VindicatorWebhook,
    WynncraftResponseUtils
)
from vindicator.constants import *

if TYPE_CHECKING:
    from vindicator.types import *


class PlayerMainInfo:

    @classmethod
    def from_raw(cls, fetched_players: lFetchedPlayers) -> List[PlayerMainInfoT]:
        ret: List[PlayerMainInfoT] = []
        for fetched_player in fetched_players:
            player_stats: PlayerStats = fetched_player["player_stats"]
            try:
                player: PlayerMainInfoT = {
                    "first_join": int(WynncraftResponseUtils.parse_datestr2(player_stats["firstJoin"])),
                    "latest_username": player_stats["username"],
                    "server": player_stats["server"],
                    "uuid": WynncraftResponseUtils.format_uuid(player_stats["uuid"]),
                }
                ret.append(player)
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
    @ErrorHandler.alock("deadlock_1")
    async def to_db(cls, fetched_players: lFetchedPlayers) -> None:
        params: List[PlayerMainInfoT] = PlayerMainInfo.from_raw(fetched_players)
        query = (
           f"INSERT INTO {PLAYER_MAIN_INFO} "
           "(first_join, latest_username, server, uuid) "
           "VALUES "
           "(%(first_join)s, %(latest_username)s, %(server)s, %(uuid)s) "
           "ON DUPLICATE KEY UPDATE "
           "latest_username = VALUES(latest_username)"
        )
        await WynncraftDataDatabase.write_many(query, params)  # type: ignore
