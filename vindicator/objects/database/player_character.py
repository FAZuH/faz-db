from __future__ import annotations
from typing import TYPE_CHECKING, List, TypedDict

from database.vindicator_database import VindicatorDatabase
from objects.wynncraft_response.player_stats import ProfessionsData
from utils.wynncraft_response_utils import WynncraftResponseUtils as WynnUtils

if TYPE_CHECKING:
    from objects.wynncraft_response.player_stats import PlayerStats
    from request.fetch_player import FetchedPlayer


class PlayerCharacter:
    TYPE = TypedDict(("PlayerCharacter"), {
        "character_uuid": bytes,  # binary(16)

        # Professions
        "alchemism": float,  # decimal(5, 2) unsigned
        "armouring": float,  # decimal(5, 2) unsigned
        "cooking": float,  # decimal(5, 2) unsigned
        "farming": float,  # decimal(5, 2) unsigned
        "fishing": float,  # decimal(5, 2) unsigned
        "jeweling": float,  # decimal(5, 2) unsigned
        "mining": float,  # decimal(5, 2) unsigned
        "scribing": float,  # decimal(5, 2) unsigned
        "tailoring": float,  # decimal(5, 2) unsigned
        "weaponsmithing": float,  # decimal(5, 2) unsigned
        "woodcutting": float,  # decimal(5, 2) unsigned
        "woodworking": float,  # decimal(5, 2) unsigned

        # Direct
        "chests_found": int,  # int unsigned
        "deaths": int,  # int unsigned
        "discoveries": int,  # int unsigned
        "level": float,  # decimal(5, 2) unsigned
        "logins": int,  # int unsigned
        "mobs_killed": int,  # int unsigned
        "playtime": int,  # int unsigned
        "wars": int,  # int unsigned
        "xp": int,  # bigint unsigned
        "dungeon_completions": int,  # int unsigned
        "quest_completions": int,  # int unsigned
        "raid_completions": int,  # int unsigned

        # Needs special computation
        "gamemode": bytes,  # bit(5)

        "unique_hash": bytes,  # binary(32)
        "timestamp": int,  # int unsigned
    })

    @staticmethod
    def from_raw(fetched_players: List["FetchedPlayer"]) -> List[PlayerCharacter.TYPE]:
        ret: List[PlayerCharacter.TYPE] = []
        for fetched_player in fetched_players:
            player_stats: "PlayerStats" = fetched_player["player_stats"]

            for character_uuid, character_info in player_stats["characters"].items():
                player_character: PlayerCharacter.TYPE = {  # type: ignore
                    "character_uuid": WynnUtils.format_uuid(character_uuid),
                    "chests_found": character_info["chestsFound"] if character_info["chestsFound"] else 0,
                    "deaths": character_info["deaths"] if character_info["deaths"] else 0,
                    "discoveries": character_info["discoveries"],
                    "level": character_info["level"],
                    "logins": character_info["logins"],
                    "mobs_killed": character_info["mobsKilled"] if character_info["mobsKilled"] else 0,
                    "playtime": character_info["playtime"],
                    "wars": character_info["wars"],
                    "xp": character_info["xp"],
                    "dungeon_completions": character_info["dungeons"]["total"] if (character_info["dungeons"] and "total" in character_info["dungeons"]) else 0,
                    "quest_completions": len(character_info["quests"]) if character_info["quests"] else 0,
                    "raid_completions": character_info["raids"]["total"] if (character_info["raids"] and "total" in character_info["raids"]) else 0,
                    "gamemode": WynnUtils.format_gamemodes(character_info["gamemode"])
                }

                # Professions
                for profession in ProfessionsData.__annotations__:
                    if character_info["professions"]:
                        level = character_info["professions"][profession]["level"]
                        xp_percent = character_info["professions"][profession]["xpPercent"]
                        player_character[profession] = float(level + (xp_percent / 100))
                    else:
                        player_character[profession] = 0.0  # For players with blank professions

                player_character["unique_hash"] = WynnUtils.compute_hash(''.join([str(value) for value in player_character.values() if value]))
                player_character["timestamp"] = int(fetched_player["response_timestamp"])
                ret.append(player_character)
        return ret

    @staticmethod
    async def to_db(fetched_players: List["FetchedPlayer"]) -> None:
        params: List[PlayerCharacter.TYPE] = PlayerCharacter.from_raw(fetched_players)
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
        await VindicatorDatabase.write_many(query, params)  # type: ignore
        print(4)
