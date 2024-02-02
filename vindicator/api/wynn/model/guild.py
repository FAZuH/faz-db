from __future__ import annotations
from typing import Any, Generator

from vindicator import BodyDateField, Nullable, UsernameOrUuidField, UuidField


class Guild:

    def __init__(self, raw: dict[str, Any]) -> None:
        self._raw = raw
        self._uuid = UuidField(raw["uuid"])
        self._name = raw["name"]
        self._prefix = raw["prefix"]
        self._level = raw["level"]
        self._xp_percent = raw["xpPercent"]
        self._territories = raw["territories"]
        self._wars = raw["wars"] or 0
        self._created = BodyDateField(raw["created"])
        self._members = Guild.Members(raw["members"])
        self._online = raw["online"]
        self._banner = Nullable(Guild.Banner, raw.get("banner", None))
        self._season_ranks = {
            season: Guild.SeasonRankInfo(season_rank_info)
            for season, season_rank_info in raw["seasonRanks"].items()
        }

    def iter_seasonranks(self) -> Generator[tuple[str, Guild.SeasonRankInfo], Any, None]:
        for rank, season_rank_info in self.season_ranks.items():
            yield rank, season_rank_info

    class Members:
        def __init__(self, node: dict[str, Any]) -> None:
            self._total = node["total"]
            self._owner = self._members_constructor(node["owner"])
            self._chief = self._members_constructor(node["chief"])
            self._strategist = self._members_constructor(node["strategist"])
            self._captain = self._members_constructor(node["captain"])
            self._recruiter = self._members_constructor(node["recruiter"])
            self._recruit = self._members_constructor(node["recruit"])

        def get_online_members(self) -> int:
            return len(tuple(self.iter_online_members()))

        def iter_online_members(self) -> Generator[tuple[str, UsernameOrUuidField, Guild.Members.MemberInfo], Any, None]:
            for rank, uuid, memberinfo in self.iter_members():
                if memberinfo.online:
                    yield (rank, uuid, memberinfo)

        def iter_members(self) -> Generator[tuple[str, UsernameOrUuidField, Guild.Members.MemberInfo], Any, None]:
            all_: dict[str, dict[UsernameOrUuidField, Guild.Members.MemberInfo]] = {
                "owner": self.owner,
                "chief": self.chief,
                "strategist": self.strategist,
                "captain": self.captain,
                "recruiter": self.recruiter,
                "recruit": self.recruit
            }
            for rank, members in all_.items():
                for identifier, member in members.items():
                    yield (rank, identifier, member)

        def _members_constructor(self, node: dict[str, Any]) -> dict[UsernameOrUuidField, Guild.Members.MemberInfo]:
            return {
                UsernameOrUuidField(identifier): Guild.Members.MemberInfo(member)
                for identifier, member in node.items()
            }

        class MemberInfo:
            def __init__(self, node: dict[str, Any]) -> None:
                self._uuid = Nullable(UuidField, node.get("uuid", None))
                self._username = node.get("username" , None)
                self._online = node["online"]
                self._server = node["server"]
                self._contributed = node["contributed"]
                self._contribution_rank = node["contributionRank"]
                self._joined = BodyDateField(node["joined"])

            @property
            def uuid(self) -> None | UuidField:
                return self._uuid

            @property
            def username(self) -> None | str:
                return self._username

            @property
            def online(self) -> bool:
                return self._online

            @property
            def server(self) -> None | str:
                return self._server

            @property
            def contributed(self) -> int:
                return self._contributed

            @property
            def contribution_rank(self) -> int:
                return self._contribution_rank

            @property
            def joined(self) -> BodyDateField:
                return self._joined

        @property
        def total(self) -> int:
            return self._total

        @property
        def owner(self) -> dict[UsernameOrUuidField, MemberInfo]:
            return self._owner

        @property
        def chief(self) -> dict[UsernameOrUuidField, MemberInfo]:
            return self._chief

        @property
        def strategist(self) -> dict[UsernameOrUuidField, MemberInfo]:
            return self._strategist

        @property
        def captain(self) -> dict[UsernameOrUuidField, MemberInfo]:
            return self._captain

        @property
        def recruiter(self) -> dict[UsernameOrUuidField, MemberInfo]:
            return self._recruiter

        @property
        def recruit(self) -> dict[UsernameOrUuidField, MemberInfo]:
            return self._recruit

    class Banner:
        def __init__(self, node: dict[str, Any]) -> None:
            self._base = node["base"]
            self._tier = node["tier"]
            self._structure = node.get("structure", None)
            self._layers = [
                Guild.Banner.LayerInfo(layer)
                for layer in node["layers"]
            ]

        class LayerInfo:
            def __init__(self, node: dict[str, Any]) -> None:
                self._colour: str = node["colour"]
                self._pattern: str = node["pattern"]

            @property
            def colour(self) -> str:
                return self._colour

            @property
            def pattern(self) -> str:
                return self._pattern

        @property
        def base(self) -> str:
            return self._base

        @property
        def tier(self) -> int:
            return self._tier

        @property
        def structure(self) -> None | str:
            return self._structure

        @property
        def layers(self) -> list[LayerInfo]:
            return self._layers

    class SeasonRankInfo:
        def __init__(self, node: dict[str, Any]) -> None:
            self._rating = node["rating"]
            self._final_territories = node["finalTerritories"]

        @property
        def rating(self) -> int:
            return self._rating

        @property
        def final_territories(self) -> int:
            return self._final_territories

    @property
    def raw(self) -> dict[str, Any]:
        return self._raw

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
    def level(self) -> int:
        return self._level

    @property
    def xp_percent(self) -> int:
        return self._xp_percent

    @property
    def territories(self) -> int:
        return self._territories

    @property
    def wars(self) -> int:
        return self._wars

    @property
    def created(self) -> BodyDateField:
        return self._created

    @property
    def members(self) -> Guild.Members:
        return self._members

    @property
    def online(self) -> int:
        return self._online

    @property
    def banner(self) -> None | Guild.Banner:
        return self._banner

    @property
    def season_ranks(self) -> dict[str, Guild.SeasonRankInfo]:
        return self._season_ranks
