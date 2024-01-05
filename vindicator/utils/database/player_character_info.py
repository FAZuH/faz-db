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


class PlayerCharacterInfo:

    @classmethod
    def from_raw(cls, fetched_players: lFetchedPlayers) -> List[PlayerCharacterInfoT]:
        ret: List[PlayerCharacterInfoT] = []
        for fetched_player in fetched_players:
            player_stats: PlayerStats = fetched_player["player_stats"]
            try:
                for character_uuid, character_info in player_stats["characters"].items():
                    ret.append({
                        "character_uuid": WynncraftResponseUtils.format_uuid(character_uuid),
                        "type": WynncraftResponseUtils.fix_chartype(character_info["type"].upper()),
                        "uuid": WynncraftResponseUtils.format_uuid(player_stats["uuid"])
                    })
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
        params: List[PlayerCharacterInfoT] = PlayerCharacterInfo.from_raw(fetched_players)
        query: str = (  # NOTE: This doesn't change. Ignore duplicates.
            f"INSERT IGNORE INTO {PLAYER_CHARACTER_INFO} (character_uuid, type, uuid) "
            "VALUES (%(character_uuid)s, %(type)s, %(uuid)s)"
        )
        await WynncraftDataDatabase.write_many(query, params)  # type: ignore
