from typing import Any

from ..model import Headers, Player
from . import AbstractWynnResponse


class PlayerResponse(AbstractWynnResponse[Player]):

    def __init__(self, body: dict[str, Any], headers: dict[str, Any]) -> None:
        super().__init__(Player(body), Headers(headers))
