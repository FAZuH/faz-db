from typing import Any

from ..model import Headers, Players
from . import AbstractWynnResponse


class PlayersResponse(AbstractWynnResponse[Players]):

    def __init__(self, body: dict[str, Any], headers: dict[str, Any]) -> None:
        super().__init__(Players(body), Headers(headers))
