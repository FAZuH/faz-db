from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional, TypedDict

from constants import DatabaseTables
from database.vindicator_database import VindicatorDatabase
from utils.wynncraft_response_utils import WynncraftResponseUtils as WynnUtils

if TYPE_CHECKING:
    from objects.wynncraft_response.player_stats import PlayerStats
    from request.fetch_player import FetchedPlayer


class PlayerMainInfo:
    TYPE = TypedDict(("PlayerMainInfo"), {
        "first_join": Optional[int],  # int unsigned
        "latest_username": str,  # varchar(16)
        "server": Optional[str],  # varchar(10)
        "timestamp": int,  # int unsigned
        "uuid": bytes,  # binary(16)
    })

    @staticmethod
    def from_raw(fetched_players: List["FetchedPlayer"]) -> List[PlayerMainInfo.TYPE]:
        ret: List[PlayerMainInfo.TYPE] = []
        for fetched_player in fetched_players:
            player_stats: "PlayerStats" = fetched_player["player_stats"]
            player: PlayerMainInfo.TYPE = {
                "first_join": int(WynnUtils.parse_datestr2(player_stats["firstJoin"])),
                "latest_username": player_stats["username"],
                "server": player_stats["server"],
                "timestamp": int(fetched_player["response_timestamp"]),
                "uuid": WynnUtils.format_uuid(player_stats["uuid"]),
            }
            ret.append(player)
        return ret

    @staticmethod
    async def to_db(fetched_players: List["FetchedPlayer"]) -> None:
        params: List[PlayerMainInfo.TYPE] = PlayerMainInfo.from_raw(fetched_players)
        query = (
           f"INSERT INTO {DatabaseTables.PLAYER_MAIN_INFO} "
           "(first_join, latest_username, server, timestamp, uuid) "
           "VALUES "
           "(%(first_join)s, %(latest_username)s, %(server)s, %(timestamp)s, %(uuid)s) "
           "ON DUPLICATE KEY UPDATE "  # NOTE: This might change. Update duplicates.
           "first_join = VALUES(first_join), "
           "latest_username = VALUES(latest_username), "
           "server = VALUES(server), "
           "timestamp = VALUES(timestamp)"
        )
        await VindicatorDatabase.write_many(query, params)  # type: ignore
        print(1)
