from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, List, Optional, Self, Tuple

from database.vindicator_database import VindicatorDatabase
from utils.wynncraft_response_utils import WynncraftResponseUtils as WynnUtils

if TYPE_CHECKING:
    from objects.wynncraft_response.player_stats import PlayerStats
    from request.fetch_player import FetchedPlayer


@dataclass
class PlayerMain:
    guild_name: Optional[str]  # NOTE: varchar(30)
    guild_rank: Optional[str]  # NOTE: enum('OWNER', 'CHIEF', 'STRATEGIST', 'CAPTAIN', 'RECRUITER', 'RECRUIT)
    playtime: int  # NOTE: int unsigned
    support_rank: Optional[str]  # NOTE: varchar(45)
    timestamp: int  # NOTE: int unsigned
    unique_hash: bytes  # NOTE: binary(32)
    username: str  # NOTE: varchar(16)
    uuid: bytes  # NOTE: binary(16)

    @classmethod
    def from_raw(cls, fetched_players: List["FetchedPlayer"]) -> List[dict]:
        ret = []

        for fetched_player in fetched_players:

            timestamp: float = fetched_player["response_datetime"]
            player_stats: "PlayerStats" = fetched_player["player_stats"]

            # NOTE: For easier hash computing
            player: PlayerMain = PlayerMain(**{key: None for key in PlayerMain.__annotations__})  # type: ignore
            player.guild_name = player_stats["guild"]["name"] if player_stats["guild"] else None
            player.guild_rank = player_stats["guild"]["rank"].upper() if player_stats["guild"] else None
            player.playtime = player_stats["playtime"]
            player.support_rank = player_stats["supportRank"]
            player.username = player_stats["username"]
            player.uuid = WynnUtils.format_uuid(player_stats["uuid"])

            player.unique_hash = WynnUtils.compute_hash(
                ''.join(
                    [str(value) for value in asdict(player).values() if value]
                )
            )

            player.timestamp = int(timestamp)

            ret.append(asdict(player))

        return ret

    @staticmethod
    async def to_db(player_main: List[dict]) -> None:
        query = (
            "INSERT INTO player_main "
            "(guild_name, guild_rank, playtime, support_rank, timestamp, unique_hash, username, uuid) "
            "VALUES "
            "(%(guild_name)s, %(guild_rank)s, %(playtime)s, %(support_rank)s, %(timestamp)s, %(unique_hash)s, %(username)s, %(uuid)s) "
            "ON DUPLICATE KEY UPDATE "
            "timestamp = VALUES(timestamp)"
        )
        await VindicatorDatabase.write_many(query=query, seq_of_params=player_main)  # type: ignore | dumb shit
        return
