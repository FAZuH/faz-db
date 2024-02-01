from typing import Any

from vindicator import Headers, Player, WynnResponse


class PlayerResponse(WynnResponse[Player]):

    def __init__(self, body: dict[str, Any], headers: dict[str, Any]) -> None:
        super().__init__(Player(body), Headers(headers))

