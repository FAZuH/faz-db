from __future__ import annotations
from typing import TYPE_CHECKING, List, TypedDict

from constants import DatabaseTables
from database.vindicator_database import VindicatorDatabase
from utils.wynncraft_response_utils import WynncraftResponseUtils as WynnUtils

if TYPE_CHECKING:
    from objects.wynncraft_response import PlayerStats
    from request.fetch_player import FetchedPlayer


class PlayerCharacterInfo:
    TYPE = TypedDict("PlayerCharacterInfo", {
        "character_uuid": bytes,  # binary(16)
        "type": str,  # enum('ARCHER', 'ASSASSIN', 'MAGE', 'SHAMAN', 'WARRIOR')
        "uuid": bytes  # binary(16)
    })

    @staticmethod
    def from_raw(fetched_players: List["FetchedPlayer"]) -> List[PlayerCharacterInfo.TYPE]:
        ret: List[PlayerCharacterInfo.TYPE] = []
        for fetched_player in fetched_players:
            player_stat: "PlayerStats" = fetched_player["player_stats"]
            for character_uuid, character_info in player_stat["characters"].items():
                ret.append({
                    "character_uuid": WynnUtils.format_uuid(character_uuid),
                    "type": WynnUtils.fix_chartype(character_info["type"].upper()),
                    "uuid": WynnUtils.format_uuid(player_stat["uuid"])
                })
        return ret

    @staticmethod
    async def to_db(fetched_players: List["FetchedPlayer"]) -> None:
        params: List[PlayerCharacterInfo.TYPE] = PlayerCharacterInfo.from_raw(fetched_players)
        query: str = (  # NOTE: This doesn't change. Ignore duplicates.
            f"INSERT IGNORE INTO {DatabaseTables.PLAYER_CHARACTER_INFO} (character_uuid, type, uuid) "
            "VALUES (%(character_uuid)s, %(type)s, %(uuid)s)"
        )
        await VindicatorDatabase.write_many(query, params)  # type: ignore
        print(2)
