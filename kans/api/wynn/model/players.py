from typing import Any, Generator

from kans import UsernameOrUuidField


class Players:

    def __init__(self, raw: dict[str, Any]) -> None:
        self._raw = raw
        self._total = raw["total"]
        self._players = {
            UsernameOrUuidField(usernameoruuid): server
            for usernameoruuid, server in raw["players"].items()
        }

    def iter_players(self) -> Generator[tuple[UsernameOrUuidField, str], Any, None]:
        for usernameoruuid, server in self._players.items():
            yield usernameoruuid, server

    @property
    def raw(self) -> dict[str, Any]:
        return self._raw

    @property
    def total(self) -> int:
        return self._total

    @property
    def players(self) -> dict[UsernameOrUuidField, str]:
        return self._players
