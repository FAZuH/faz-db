from typing import TYPE_CHECKING, List, Self, Tuple
from dataclasses import dataclass, asdict

from database.vindicator_database import VindicatorDatabase
from utils.wynncraft_response_utils import WynncraftResponseUtils as WynnUtils

if TYPE_CHECKING:
    from objects.wynncraft_response.player_stats import PlayerStats, ProfessionsData
    from request.fetch_player import FetchedPlayer


@dataclass
class PlayerCharacter:
    character_uuid: bytes  # binary(16)

    # NOTE: Professions
    alchemism: float  # decimal(5, 2) unsigned
    armouring: float  # decimal(5, 2) unsigned
    cooking: float  # decimal(5, 2) unsigned
    character_uuid: bytes  # binary(16)
    farming: float  # decimal(5, 2) unsigned
    fishing: float  # decimal(5, 2) unsigned
    jeweling: float  # decimal(5, 2) unsigned
    mining: float  # decimal(5, 2) unsigned
    scribing: float  # decimal(5, 2) unsigned
    tailoring: float  # decimal(5, 2) unsigned
    weaponsmithing: float  # decimal(5, 2) unsigned
    woodcutting: float  # decimal(5, 2) unsigned
    woodworking: float  # decimal(5, 2) unsigned

    # NOTE: Direct
    chests_found: int  # int unsigned
    deaths: int  # int unsigned
    discoveries: int  # int unsigned
    level: float  # decimal(5, 2) unsigned
    logins: int  # int unsigned
    mobs_killed: int  # int unsigned
    playtime: int  # int unsigned
    wars: int  # int unsigned
    xp: int  # bigint unsigned
    dungeon_completions: int  # int unsigned
    quest_completions: int  # int unsigned
    raid_completions: int  # int unsigned

    # NOTE: Needs special computation
    gamemode: bytes  # bit(5)
    timestamp: int  # int unsigned
    unique_hash: bytes  # binary(32)

    @classmethod
    def from_raw(cls, fetched_players: List["FetchedPlayer"]) -> List[dict]:
        ret: List[dict] = []

        for fetched_player in fetched_players:

            timestamp: float = fetched_player["response_datetime"]
            player_stats: "PlayerStats" = fetched_player["player_stats"]

            for character_uuid, character_info in player_stats["characters"].items():

                # NOTE: For easier hash computing
                character: PlayerCharacter = cls(**{key: None for key in cls.__annotations__})  # type: ignore
                character.character_uuid = WynnUtils.format_uuid(character_uuid)

                # NOTE: Professions
                for profession in ProfessionsData.__annotations__:
                    if not character_info["professions"]:  # NOTE: For players with blank professions
                        setattr(character, profession, 0.0)
                        continue
                    level = character_info["professions"][profession]["level"]
                    xp_percent = character_info["professions"][profession]["xpPercent"]
                    setattr(character, profession, float(level + (xp_percent / 100)))

                # NOTE: Direct
                character.chests_found = character_info["chestsFound"] if character_info["chestsFound"] else 0
                character.deaths = character_info["deaths"] if character_info["deaths"] else 0
                character.discoveries = character_info["discoveries"]
                character.level = character_info["level"]
                character.logins = character_info["logins"]
                character.mobs_killed = character_info["mobsKilled"] if character_info["mobsKilled"] else 0
                character.playtime = character_info["playtime"]
                character.wars = character_info["wars"]
                character.xp = character_info["xp"]
                character.dungeon_completions = character_info["dungeons"]["total"] if (character_info["dungeons"] and "total" in character_info["dungeons"]) else 0
                character.quest_completions = len(character_info["quests"])
                character.raid_completions = character_info["raids"]["total"] if (character_info["raids"] and "total" in character_info["raids"]) else 0

                # NOTE: Needs special computation
                character.gamemode = WynnUtils.format_gamemodes(character_info["gamemode"])
                character.unique_hash = WynnUtils.compute_hash(
                    ''.join(
                        [str(value) for value in asdict(character).values() if value]
                    )
                )
                character.timestamp = int(timestamp)
                ret.append(asdict(character))

        return ret

    @staticmethod
    async def to_db(player_characters: List[dict]) -> None:
        query = (
            "REPLACE INTO player_character ("
            "character_uuid, alchemism, armouring, cooking, farming, fishing, jeweling, mining, "
            "scribing, tailoring, weaponsmithing, woodcutting, woodworking, chests_found, deaths, "
            "discoveries, level, logins, mobs_killed, playtime, wars, xp, dungeon_completions, "
            "quest_completions, raid_completions, gamemode, timestamp, unique_hash) "
            "VALUES ("
            "%(character_uuid)s, %(alchemism)s, %(armouring)s, %(cooking)s, %(farming)s, "
            "%(fishing)s, %(jeweling)s, %(mining)s, %(scribing)s, %(tailoring)s, %(weaponsmithing)s, "
            "%(woodcutting)s, %(woodworking)s, %(chests_found)s, %(deaths)s, %(discoveries)s, %(level)s, "
            "%(logins)s, %(mobs_killed)s, %(playtime)s, %(wars)s, %(xp)s, %(dungeon_completions)s, "
            "%(quest_completions)s, %(raid_completions)s, %(gamemode)s, %(timestamp)s, %(unique_hash)s)"
        )
        await VindicatorDatabase.write_many(query=query, seq_of_params=player_characters)  # type: ignore | dumb shit
        return
