from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, List, Optional, Self, Tuple

from database.vindicator_database import VindicatorDatabase
from utils.wynncraft_response_utils import WynncraftResponseUtils as WynnUtils

if TYPE_CHECKING:
    from objects.wynncraft_response.player_stats import PlayerStats
    from request.fetch_player import FetchedPlayer


@dataclass
class PlayerMainInfo:
    first_join: Optional[int]  # NOTE: int unsigned
    latest_username: str  # NOTE: varchar(16)
    server: Optional[str]  # NOTE: varchar(10)
    timestamp: int  # NOTE: int unsigned
    uuid: bytes  # NOTE: binary(16)

    @classmethod
    def from_raw(cls, fetched_players: List["FetchedPlayer"]) -> List[dict]:
        ret = []

        for fetched_player in fetched_players:

            timestamp: float = fetched_player["response_datetime"]
            player_stats: "PlayerStats" = fetched_player["player_stats"]

            player = cls(
                first_join=int(WynnUtils.parse_datestr2(player_stats["firstJoin"])),
                latest_username=player_stats["username"],
                server=player_stats["server"],
                timestamp=int(timestamp),
                uuid=WynnUtils.format_uuid(player_stats["uuid"]),
            )
            ret.append(asdict(player))

        return ret

    @staticmethod
    async def to_db(player_main_info: List[dict]) -> None:
        query = (
           "INSERT INTO player_main_info "
           "(first_join, latest_username, server, timestamp, uuid) "
           "VALUES "
           "(%(first_join)s, %(latest_username)s, %(server)s, %(timestamp)s, %(uuid)s) "
           "ON DUPLICATE KEY UPDATE "
           "first_join = VALUES(first_join), "
           "latest_username = VALUES(latest_username), "
           "server = VALUES(server), "
           "timestamp = VALUES(timestamp)"
        )
        await VindicatorDatabase.write_many(query=query, seq_of_params=player_main_info)  # type: ignore | dumb shit
        return
