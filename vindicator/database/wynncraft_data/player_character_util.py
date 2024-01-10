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


class PlayerCharacterUtil:

    def __init__(self, fetched_players: List[FetchedPlayer]) -> None:
        self._to_insert: List[PlayerCharacterDB_I] = []
        for fetched_player in fetched_players:
            player_stats: PlayerStats = fetched_player["player_stats"]
            try:
                for character_uuid, character_info in player_stats["characters"].items():
                    player_character: PlayerCharacterDB_I = {  # type: ignore
                        "character_uuid": WynncraftResponseUtil.format_uuid(character_uuid),
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
                        "gamemode": WynncraftResponseUtil.format_gamemodes(character_info["gamemode"])
                    }

                    # Professions
                    for profession in ProfessionsData.__annotations__:
                        if character_info["professions"]:
                            level: int = character_info["professions"][profession]["level"]
                            xp_percent: int = character_info["professions"][profession]["xpPercent"]
                            decimal_level: float = float(level + (xp_percent / 100))
                            decimal_level = decimal_level if decimal_level >= 1.0 else 1.0
                            player_character[profession] = decimal_level
                        else:
                            player_character[profession] = 1.0  # For players with blank professions

                    player_character["unique_hash"] = WynncraftResponseUtil.compute_hash(''.join([str(value) for value in player_character.values() if value]))
                    player_character["datetime"] = fetched_player["resp_datetime"]
                    self._to_insert.append(player_character)
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

    async def to_db(self) -> None:
        query = (
            f"REPLACE INTO {PLAYER_CHARACTER} ("
            "character_uuid, alchemism, armouring, cooking, farming, fishing, jeweling, mining, "
            "scribing, tailoring, weaponsmithing, woodcutting, woodworking, chests_found, deaths, "
            "discoveries, level, logins, mobs_killed, playtime, wars, xp, dungeon_completions, "
            "quest_completions, raid_completions, gamemode, datetime, unique_hash) "
            "VALUES ("
            "%(character_uuid)s, %(alchemism)s, %(armouring)s, %(cooking)s, %(farming)s, "
            "%(fishing)s, %(jeweling)s, %(mining)s, %(scribing)s, %(tailoring)s, %(weaponsmithing)s, "
            "%(woodcutting)s, %(woodworking)s, %(chests_found)s, %(deaths)s, %(discoveries)s, %(level)s, "
            "%(logins)s, %(mobs_killed)s, %(playtime)s, %(wars)s, %(xp)s, %(dungeon_completions)s, "
            "%(quest_completions)s, %(raid_completions)s, %(gamemode)s, %(datetime)s, %(unique_hash)s)"
        )
        await WynncraftDataDatabase.execute(query, self._to_insert)
