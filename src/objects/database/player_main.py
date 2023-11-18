from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional, TypedDict

from database.vindicator_database import VindicatorDatabase
from utils.wynncraft_response_utils import WynncraftResponseUtils as WynnUtils

if TYPE_CHECKING:
    from objects.wynncraft_response.player_stats import PlayerStats
    from request.fetch_player import FetchedPlayer


class PlayerMain:
    TYPE = TypedDict("PlayerMain", {
        "guild_name": Optional[str],  # varchar(30)
        "guild_rank": Optional[str],  # enum('OWNER', 'CHIEF', 'STRATEGIST', 'CAPTAIN', 'RECRUITER', 'RECRUIT)
        "playtime": int,  # int unsigned
        "support_rank": Optional[str],  # varchar(45)
        "username": str,  # varchar(16)
        "uuid": bytes,  # binary(16)

        "unique_hash": bytes,  # binary(32)
        "timestamp": int,  # int unsigned
    }, total=False)

    @staticmethod
    def from_raw(fetched_players: List["FetchedPlayer"]) -> List[PlayerMain.TYPE]:
        ret: List[PlayerMain.TYPE] = []
        for fetched_player in fetched_players:
            player_stats: "PlayerStats" = fetched_player["player_stats"]
            player_main: PlayerMain.TYPE = {
                "guild_name" : player_stats["guild"]["name"] if player_stats["guild"] else None,
                "guild_rank" : player_stats["guild"]["rank"].upper() if player_stats["guild"] else None,
                "playtime" : player_stats["playtime"],
                "support_rank" : player_stats["supportRank"],
                "username" : player_stats["username"],
                "uuid" : WynnUtils.format_uuid(player_stats["uuid"])
            }
            player_main["unique_hash"] = WynnUtils.compute_hash(''.join([str(value) for value in player_main.values() if value]))
            player_main["timestamp"] = int(fetched_player["response_timestamp"])
            ret.append(player_main)
        return ret

    @staticmethod
    async def to_db(fetched_players: List["FetchedPlayer"]) -> None:
        params: List[PlayerMain.TYPE] = PlayerMain.from_raw(fetched_players)
        query = (
            "INSERT INTO player_main "
            "(guild_name, guild_rank, playtime, support_rank, timestamp, unique_hash, username, uuid) "
            "VALUES "
            "(%(guild_name)s, %(guild_rank)s, %(playtime)s, %(support_rank)s, %(timestamp)s, %(unique_hash)s, %(username)s, %(uuid)s) "
            "ON DUPLICATE KEY UPDATE "
            "timestamp = VALUES(timestamp)"
        )
        await VindicatorDatabase.write_many(query, params)  # type: ignore
        return
