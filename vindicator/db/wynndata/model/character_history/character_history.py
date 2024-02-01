from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING, Self
from typing_extensions import override

from vindicator import CharacterHistoryId, DateColumn, GamemodeColumn, UuidColumn

if TYPE_CHECKING:
    from vindicator import PlayerResponse


class CharacterHistory(CharacterHistoryId):
    """id: character_uuid, datetime"""

    def __init__(
        self,
        character_uuid: UuidColumn,
        level: int,
        xp: int,
        wars: int,
        playtime: Decimal,
        mobs_killed: int,
        chests_found: int,
        logins: int,
        deaths: int,
        discoveries: int,
        gamemode: GamemodeColumn,
        alchemism: Decimal,
        armouring: Decimal,
        cooking: Decimal,
        jeweling: Decimal,
        scribing: Decimal,
        tailoring: Decimal,
        weaponsmithing: Decimal,
        woodworking: Decimal,
        mining: Decimal,
        woodcutting: Decimal,
        farming: Decimal,
        fishing: Decimal,
        dungeon_completions: int,
        quest_completions: int,
        raid_completions: int,
        datetime: DateColumn
    ) -> None:
        self._character_uuid = character_uuid
        self._level = level
        self._xp = xp
        self._wars = wars
        self._playtime = playtime
        self._mobs_killed = mobs_killed
        self._chests_found = chests_found
        self._logins = logins
        self._deaths = deaths
        self._discoveries = discoveries
        self._gamemode = gamemode
        self._alchemism = alchemism
        self._armouring = armouring
        self._cooking = cooking
        self._jeweling = jeweling
        self._scribing = scribing
        self._tailoring = tailoring
        self._weaponsmithing = weaponsmithing
        self._woodworking = woodworking
        self._mining = mining
        self._woodcutting = woodcutting
        self._farming = farming
        self._fishing = fishing
        self._dungeon_completions = dungeon_completions
        self._quest_completions = quest_completions
        self._raid_completions = raid_completions
        self._datetime = datetime

    @classmethod
    def from_response(cls, response: PlayerResponse) -> list[CharacterHistory]:
        return [
            cls(
                character_uuid=UuidColumn(character_uuid.to_bytes()),
                level=character.level,
                xp=character.xp,
                wars=character.wars,
                playtime=Decimal(character.playtime),
                mobs_killed=character.mobs_killed,
                chests_found=character.chests_found,
                logins=character.logins,
                deaths=character.deaths,
                discoveries=character.discoveries,
                gamemode=GamemodeColumn(character.gamemode.to_bytes()),
                alchemism=Decimal(character.professions.alchemism.to_float()),
                armouring=Decimal(character.professions.armouring.to_float()),
                cooking=Decimal(character.professions.cooking.to_float()),
                jeweling=Decimal(character.professions.jeweling.to_float()),
                scribing=Decimal(character.professions.scribing.to_float()),
                tailoring=Decimal(character.professions.tailoring.to_float()),
                weaponsmithing=Decimal(character.professions.weaponsmithing.to_float()),
                woodworking=Decimal(character.professions.woodworking.to_float()),
                mining=Decimal(character.professions.mining.to_float()),
                woodcutting=Decimal(character.professions.woodcutting.to_float()),
                farming=Decimal(character.professions.farming.to_float()),
                fishing=Decimal(character.professions.fishing.to_float()),
                dungeon_completions=character.dungeons.total,
                quest_completions=len(character.quests),
                raid_completions=character.raids.total,
                datetime=DateColumn(response.get_datetime())
            ) for character_uuid, character in response.body.iter_characters()
        ]

    @property
    @override
    def character_uuid(self) -> UuidColumn:
        return self._character_uuid

    @property
    def level(self) -> int:
        return self._level

    @property
    def xp(self) -> int:
        return self._xp

    @property
    def wars(self) -> int:
        return self._wars

    @property
    def playtime(self) -> Decimal:
        return self._playtime

    @property
    def mobs_killed(self) -> int:
        return self._mobs_killed

    @property
    def chests_found(self) -> int:
        return self._chests_found

    @property
    def logins(self) -> int:
        return self._logins

    @property
    def deaths(self) -> int:
        return self._deaths

    @property
    def discoveries(self) -> int:
        return self._discoveries

    @property
    def gamemode(self) -> GamemodeColumn:
        return self._gamemode

    @property
    def alchemism(self) -> Decimal:
        return self._alchemism

    @property
    def armouring(self) -> Decimal:
        return self._armouring

    @property
    def cooking(self) -> Decimal:
        return self._cooking

    @property
    def jeweling(self) -> Decimal:
        return self._jeweling

    @property
    def scribing(self) -> Decimal:
        return self._scribing

    @property
    def tailoring(self) -> Decimal:
        return self._tailoring

    @property
    def weaponsmithing(self) -> Decimal:
        return self._weaponsmithing

    @property
    def woodworking(self) -> Decimal:
        return self._woodworking

    @property
    def mining(self) -> Decimal:
        return self._mining

    @property
    def woodcutting(self) -> Decimal:
        return self._woodcutting

    @property
    def farming(self) -> Decimal:
        return self._farming

    @property
    def fishing(self) -> Decimal:
        return self._fishing

    @property
    def dungeon_completions(self) -> int:
        return self._dungeon_completions

    @property
    def quest_completions(self) -> int:
        return self._quest_completions

    @property
    def raid_completions(self) -> int:
        return self._raid_completions

    @property
    @override
    def datetime(self) -> DateColumn:
        return self._datetime
