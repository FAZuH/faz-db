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


class PlayerCharacterInfoUtil:

    def __init__(self, fetched_players: List[FetchedPlayer]) -> None:
        self._to_insert: List[PlayerCharacterInfoDB_I] = []
        for fetched_player in fetched_players:
            player_stats: PlayerStats = fetched_player["player_stats"]
            try:
                for character_uuid, character_info in player_stats["characters"].items():
                    self._to_insert.append({
                        "character_uuid": WynncraftResponseUtil.format_uuid(character_uuid),
                        "type": WynncraftResponseUtil.fix_chartype(character_info["type"].upper()),
                        "uuid": WynncraftResponseUtil.format_uuid(player_stats["uuid"])
                    })
            except Exception as e:
                try:
                    error_message = {
                        "error": str(e),
                        "data recipient": PLAYER_CHARACTER_INFO,
                        "username": player_stats["username"],
                        "timestamp": f"<t:{int(time())}>",
                    }
                except Exception as e:
                    error_message: dict = {"error": str(e), "message": "Failed building error message."}
                create_task(VindicatorWebhook.log("error", "error", error_message, title="Wynn response parsing"))
                continue

    async def to_db(self) -> None:
        query: str = (  # NOTE: This doesn't change. Ignore duplicates.
            f"INSERT IGNORE INTO {PLAYER_CHARACTER_INFO} (character_uuid, type, uuid) "
            "VALUES (%(character_uuid)s, %(type)s, %(uuid)s)"
        )
        await WynncraftDataDatabase.execute(query, self._to_insert)
