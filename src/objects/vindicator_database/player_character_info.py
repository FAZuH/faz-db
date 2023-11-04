from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, List, Tuple, Self

from database.vindicator_database import VindicatorDatabase
from utils.wynncraft_response_utils import WynncraftResponseUtils as WynnUtils

if TYPE_CHECKING:
    from objects.wynncraft_response import PlayerStats
    from request.fetch_player import FetchedPlayer


@dataclass
class PlayerCharacterInfo:
    character_uuid: bytes  # NOTE: binary(16)
    type: str  # NOTE: enum('ARCHER', 'ASSASSIN', 'MAGE', 'SHAMAN', 'WARRIOR')
    uuid: bytes  # NOTE: binary(16)

    @classmethod
    def from_raw(cls, fetched_players: List["FetchedPlayer"]) -> List[dict]:
        ret = []

        for fetched_player in fetched_players:

            player_stat: "PlayerStats" = fetched_player["player_stats"]

            for character_uuid, character_info in player_stat["characters"].items():
                character = cls(
                    character_uuid=WynnUtils.format_uuid(character_uuid),
                    type=WynnUtils.fix_chartype(character_info["type"].upper()),
                    uuid=WynnUtils.format_uuid(player_stat["uuid"])
                )
                ret.append(asdict(character))

        return ret

    @staticmethod
    async def to_db(player_character_info: List[dict]) -> None:
        query: str = (
            "INSERT IGNORE INTO player_character_info (character_uuid, type, uuid) "
            "VALUES (%(character_uuid)s, %(type)s, %(uuid)s)"
        )
        await VindicatorDatabase.write_many(query, player_character_info)
        return
