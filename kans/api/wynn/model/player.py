from __future__ import annotations
from decimal import Decimal
from typing import Any, Generator

from .field import (
    BodyDateField,
    CharacterTypeField,
    GamemodeField,
    Nullable,
    UuidField
)


class Player:

    def __init__(self, raw: dict[str, Any]) -> None:
        self._raw = raw
        self._username = raw["username"]
        self._online = raw["online"]
        self._server = raw["server"]
        self._active_character = Nullable(UuidField, raw["activeCharacter"])
        self._uuid = UuidField(raw["uuid"])
        self._rank = raw["rank"]
        self._rank_badge = raw["rankBadge"]
        self._legacy_rank_colour = Nullable(self.LegacyRankColour, raw.get("legacyRankColour"))
        self._shortened_rank = raw["shortenedRank"]
        self._support_rank = raw["supportRank"]
        self._veteran = raw["veteran"] or False
        self._first_join = BodyDateField(raw["firstJoin"])
        self._last_join = BodyDateField(raw["lastJoin"])
        self._playtime = Decimal(raw["playtime"])
        self._guild = Nullable(self.Guild, raw.get("guild"))
        self._global_data = self.GlobalData(raw["globalData"])
        self._forum_link = raw["forumLink"]
        self._ranking = raw["ranking"]
        """`rankingName: nthRank`"""
        self._public_profile = raw["publicProfile"]
        self._characters = {
            UuidField(character_uuid): self.Character(character)
            for character_uuid, character in raw["characters"].items()
        }

    def get_character_uuids(self) -> list[UuidField]:
        return list(self.characters.keys())

    def iter_characters(self) -> Generator[tuple[UuidField, Player.Character], Any, None]:
        for character_uuid, character in self._characters.items():
            yield (character_uuid, character)

    class LegacyRankColour:
        def __init__(self, node: dict[str, str]) -> None:
            self._main = node["main"]
            self._sub = node["sub"]

        @property
        def main(self) -> str:
            return self._main

        @property
        def sub(self) -> str:
            return self._sub

    class Guild:
        def __init__(self, node: dict[str, Any]) -> None:
            self._uuid = UuidField(node["uuid"])
            self._name = node["name"]
            self._prefix = node["prefix"]
            self._rank = node["rank"]
            self._rank_stars = node["rankStars"]

        @property
        def uuid(self) -> UuidField:
            return self._uuid

        @property
        def name(self) -> str:
            return self._name

        @property
        def prefix(self) -> str:
            return self._prefix

        @property
        def rank(self) -> str:
            return self._rank

        @property
        def rank_stars(self) -> None | str:
            return self._rank_stars

    class GlobalData:
        def __init__(self, node: dict[str, Any]) -> None:
            self._wars = node["wars"]
            self._total_level = node["totalLevel"]
            self._killed_mobs = node["killedMobs"]
            self._chests_found = node["chestsFound"]
            self._dungeons = Player.Dungeons(node["dungeons"])
            self._raids = Player.Raids(node["raids"])
            self._completed_quests = node["completedQuests"]
            self._pvp = Player.Pvp(node["pvp"])

        @property
        def wars(self) -> int:
            return self._wars

        @property
        def total_level(self) -> int:
            return self._total_level

        @property
        def killed_mobs(self) -> int:
            return self._killed_mobs

        @property
        def chests_found(self) -> int:
            return self._chests_found

        @property
        def dungeons(self) -> Player.Dungeons:
            return self._dungeons

        @property
        def raids(self) -> Player.Raids:
            return self._raids

        @property
        def completed_quests(self) -> int:
            return self._completed_quests

        @property
        def pvp(self) -> Player.Pvp:
            return self._pvp

    class Dungeons:
        def __init__(self, node: dict[str, Any]) -> None:
            self._total = node.get("total", 0)
            self._list = node.get("list", {})

        @property
        def total(self) -> int:
            return self._total

        @property
        def list(self) -> dict[str, int]:
            """`dungeonName: completions`"""
            return self._list

    class Raids:
        def __init__(self, node: dict[str, Any]) -> None:
            self._total = node.get("total", 0)
            self._list = node.get("list", {})

        @property
        def total(self) -> int:
            return self._total

        @property
        def list(self) -> dict[str, int]:
            """`raidName: completions`"""
            return self._list

    class Pvp:
        def __init__(self, node: dict[str, Any]) -> None:
            self._kills = node.get("kills", 0) or 0
            self._deaths = node.get("deaths", 0) or 0

        @property
        def kills(self) -> int:
            return self._kills

        @property
        def deaths(self) -> int:
            return self._deaths

    class Character:
        def __init__(self, node: dict[str, Any]) -> None:
            self._type = CharacterTypeField(node["type"])
            self._nickname = node["nickname"]
            self._level = node["level"]
            self._xp = node["xp"]
            self._xp_percent = node["xpPercent"]
            self._total_level = node["totalLevel"]
            self._wars = node["wars"]
            self._playtime = Decimal(node["playtime"])
            self._mobs_killed = node["mobsKilled"]
            self._chests_found = node["chestsFound"]
            self._items_identified = node["itemsIdentified"] or 0
            self._blocks_walked = node["blocksWalked"]
            self._logins = node["logins"]
            self._deaths = node["deaths"]
            self._discoveries = node["discoveries"]
            self._pre_economy = node["preEconomy"] or False
            self._pvp = Player.Pvp(node["pvp"])
            self._gamemode = GamemodeField(node["gamemode"])
            self._skill_points = self.SkillPoints(node["skillPoints"])
            self._professions = self.Professions(node["professions"])
            self._dungeons = Player.Dungeons(node.get("dungeons", {}) or {})
            self._raids = Player.Raids(node.get("raids", {}) or {})
            self._quests = node["quests"]

        class SkillPoints:
            def __init__(self, node: dict[str, Any]) -> None:
                self._earth = node.get("earth", 0)
                self._thunder = node.get("thunder", 0)
                self._water = node.get("water", 0)
                self._fire = node.get("fire", 0)
                self._air = node.get("air", 0)

            @property
            def earth(self) -> int:
                return self._earth

            @property
            def thunder(self) -> int:
                return self._thunder

            @property
            def water(self) -> int:
                return self._water

            @property
            def fire(self) -> int:
                return self._fire

            @property
            def air(self) -> int:
                return self._air

        class Professions:
            def __init__(self, node: dict[str, Any]) -> None:
                ProfessionInfo = self.ProfessionInfo
                self._alchemism = ProfessionInfo(node.get("alchemism", {}))
                self._armouring = ProfessionInfo(node.get("armouring", {}))
                self._cooking = ProfessionInfo(node.get("cooking", {}))
                self._farming = ProfessionInfo(node.get("farming", {}))
                self._fishing = ProfessionInfo(node.get("fishing", {}))
                self._jeweling = ProfessionInfo(node.get("jeweling", {}))
                self._mining = ProfessionInfo(node.get("mining", {}))
                self._scribing = ProfessionInfo(node.get("scribing", {}))
                self._tailoring = ProfessionInfo(node.get("tailoring", {}))
                self._weaponsmithing = ProfessionInfo(node.get("weaponsmithing", {}))
                self._woodcutting = ProfessionInfo(node.get("woodcutting", {}))
                self._woodworking = ProfessionInfo(node.get("woodworking", {}))

            class ProfessionInfo:
                def __init__(self, node: dict[str, Any]) -> None:
                    self._level = node.get("level", 0)
                    self._xp_percent = node.get("xpPercent", 0)

                def to_decimal(self) -> Decimal:
                    return self.level + (Decimal(self.xp_percent) / 100)

                @property
                def level(self) -> int:
                    return self._level

                @property
                def xp_percent(self) -> int:
                    return self._xp_percent

            @property
            def alchemism(self) -> Player.Character.Professions.ProfessionInfo:
                return self._alchemism

            @property
            def armouring(self) -> Player.Character.Professions.ProfessionInfo:
                return self._armouring

            @property
            def cooking(self) -> Player.Character.Professions.ProfessionInfo:
                return self._cooking

            @property
            def farming(self) -> Player.Character.Professions.ProfessionInfo:
                return self._farming

            @property
            def fishing(self) -> Player.Character.Professions.ProfessionInfo:
                return self._fishing

            @property
            def jeweling(self) -> Player.Character.Professions.ProfessionInfo:
                return self._jeweling

            @property
            def mining(self) -> Player.Character.Professions.ProfessionInfo:
                return self._mining

            @property
            def scribing(self) -> Player.Character.Professions.ProfessionInfo:
                return self._scribing

            @property
            def tailoring(self) -> Player.Character.Professions.ProfessionInfo:
                return self._tailoring

            @property
            def weaponsmithing(self) -> Player.Character.Professions.ProfessionInfo:
                return self._weaponsmithing

            @property
            def woodcutting(self) -> Player.Character.Professions.ProfessionInfo:
                return self._woodcutting

            @property
            def woodworking(self) -> Player.Character.Professions.ProfessionInfo:
                return self._woodworking

        # Make character properties
        @property
        def type(self) -> CharacterTypeField:
            return self._type

        @property
        def nickname(self) -> None | str:
            return self._nickname

        @property
        def level(self) -> int:
            return self._level

        @property
        def xp(self) -> int:
            return self._xp

        @property
        def xp_percent(self) -> int:
            return self._xp_percent

        @property
        def total_level(self) -> int:
            return self._total_level

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
        def items_identified(self) -> int:
            return self._items_identified

        @property
        def blocks_walked(self) -> int:
            return self._blocks_walked

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
        def pre_economy(self) -> bool:
            return self._pre_economy

        @property
        def pvp(self) -> Player.Pvp:
            return self._pvp

        @property
        def gamemode(self) -> GamemodeField:
            """list of enabled gamemodes."""
            return self._gamemode

        @property
        def skill_points(self) -> Player.Character.SkillPoints:
            return self._skill_points

        @property
        def professions(self) -> Player.Character.Professions:
            return self._professions

        @property
        def dungeons(self) -> Player.Dungeons:
            return self._dungeons

        @property
        def raids(self) -> Player.Raids:
            return self._raids

        @property
        def quests(self) -> list[str]:
            return self._quests

    @property
    def raw(self) -> dict[str, Any]:
        return self._raw

    @property
    def username(self) -> str:
        return self._username

    @property
    def online(self) -> bool:
        return self._online

    @property
    def server(self) -> None | str:
        return self._server

    @property
    def active_character(self) -> None | UuidField:
        return self._active_character

    @property
    def uuid(self) -> UuidField:
        return self._uuid

    @property
    def rank(self) -> str:
        return self._rank

    @property
    def rank_badge(self) -> None | str:
        return self._rank_badge

    @property
    def legacy_rank_colour(self) -> None | Player.LegacyRankColour:
        return self._legacy_rank_colour

    @property
    def shortened_rank(self) -> None | str:
        return self._shortened_rank

    @property
    def support_rank(self) -> None | str:
        return self._support_rank

    @property
    def veteran(self) -> bool:
        return self._veteran

    @property
    def first_join(self) -> BodyDateField:
        return self._first_join

    @property
    def last_join(self) -> BodyDateField:
        return self._last_join

    @property
    def playtime(self) -> Decimal:
        return self._playtime

    @property
    def guild(self) -> None | Player.Guild:
        return self._guild

    @property
    def global_data(self) -> Player.GlobalData:
        return self._global_data

    @property
    def forum_link(self) -> None | int:
        return self._forum_link

    @property
    def ranking(self) -> dict[str, int]:
        return self._ranking

    @property
    def public_profile(self) -> bool:
        return self._public_profile

    @property
    def characters(self) -> dict[UuidField, Player.Character]:
        return self._characters
