from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING, Iterable
from typing_extensions import override

from kans import CharacterHistoryId, DateColumn, GamemodeColumn, UuidColumn

if TYPE_CHECKING:
    from kans import PlayerResponse


class CharacterHistory(CharacterHistoryId):
    """implements `CharacterHistoryId`

    id: `character_uuid`, `datetime`"""

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
    def from_responses(cls, resps: Iterable[PlayerResponse]) -> tuple[CharacterHistory, ...]:
        return tuple(
            cls(
                character_uuid=UuidColumn(ch_uuid.to_bytes()),
                level=ch.level,
                xp=ch.xp,
                wars=ch.wars,
                playtime=Decimal(ch.playtime),
                mobs_killed=ch.mobs_killed,
                chests_found=ch.chests_found,
                logins=ch.logins,
                deaths=ch.deaths,
                discoveries=ch.discoveries,
                gamemode=GamemodeColumn(ch.gamemode.to_bytes()),
                alchemism=Decimal(ch.professions.alchemism.to_float()),
                armouring=Decimal(ch.professions.armouring.to_float()),
                cooking=Decimal(ch.professions.cooking.to_float()),
                jeweling=Decimal(ch.professions.jeweling.to_float()),
                scribing=Decimal(ch.professions.scribing.to_float()),
                tailoring=Decimal(ch.professions.tailoring.to_float()),
                weaponsmithing=Decimal(ch.professions.weaponsmithing.to_float()),
                woodworking=Decimal(ch.professions.woodworking.to_float()),
                mining=Decimal(ch.professions.mining.to_float()),
                woodcutting=Decimal(ch.professions.woodcutting.to_float()),
                farming=Decimal(ch.professions.farming.to_float()),
                fishing=Decimal(ch.professions.fishing.to_float()),
                dungeon_completions=ch.dungeons.total,
                quest_completions=len(ch.quests),
                raid_completions=ch.raids.total,
                datetime=DateColumn(resp.get_datetime())
            ) for resp in resps for ch_uuid, ch in resp.body.iter_characters()
        )

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
