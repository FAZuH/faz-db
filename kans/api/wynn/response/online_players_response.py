from typing import Any

from ..model import Headers, OnlinePlayers
from . import AbstractWynnResponse


class OnlinePlayersResponse(AbstractWynnResponse[OnlinePlayers]):

    def __init__(self, body: dict[str, Any], headers: dict[str, Any]) -> None:
        super().__init__(OnlinePlayers(body), Headers(headers))
