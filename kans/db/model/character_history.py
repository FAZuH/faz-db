from __future__ import annotations
from typing import TYPE_CHECKING

from kans import DateColumn, GamemodeColumn, UuidColumn

if TYPE_CHECKING:
    from datetime import datetime as dt
    from decimal import Decimal


class CharacterHistory:
    """id: `character_uuid`, `datetime`"""

    def __init__(
        self,
        character_uuid: bytes | UuidColumn,
        level: int,
        xp: int,
        wars: int,
        playtime: Decimal,
        mobs_killed: int,
        chests_found: int,
        logins: int,
        deaths: int,
        discoveries: int,
        gamemode: bytes | GamemodeColumn,
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
        datetime: dt | DateColumn
    ) -> None:
        self._character_uuid = character_uuid if isinstance(character_uuid, UuidColumn) else UuidColumn(character_uuid)
        self._level = level
        self._xp = xp
        self._wars = wars
        self._playtime = playtime
        self._mobs_killed = mobs_killed
        self._chests_found = chests_found
        self._logins = logins
        self._deaths = deaths
        self._discoveries = discoveries
        self._gamemode = gamemode if isinstance(gamemode, GamemodeColumn) else GamemodeColumn(gamemode)
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
        self._datetime = datetime if isinstance(datetime, DateColumn) else DateColumn(datetime)

    @property
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
    def datetime(self) -> DateColumn:
        return self._datetime
