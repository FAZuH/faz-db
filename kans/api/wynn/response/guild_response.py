from typing import Any

from ..model import Guild, Headers
from . import AbstractWynnResponse


class GuildResponse(AbstractWynnResponse[Guild]):

    def __init__(self, body: dict[str, Any], headers: dict[str, Any]) -> None:
        super().__init__(Guild(body), Headers(headers))
