from typing import Any

from kans import Headers, Players, WynnResponse


class PlayersResponse(WynnResponse[Players]):

    def __init__(self, body: dict[str, Any], headers: dict[str, Any]) -> None:
        super().__init__(Players(body), Headers(headers))
