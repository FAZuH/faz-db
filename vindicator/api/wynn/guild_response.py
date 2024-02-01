from typing import Any

from vindicator import Guild, Headers, WynnResponse


class GuildResponse(WynnResponse[Guild]):

    def __init__(self, body: dict[str, Any], headers: dict[str, Any]) -> None:
        super().__init__(Guild(body), Headers(headers))
