from __future__ import annotations
from typing import Any, TYPE_CHECKING

from .._http_request import HttpRequest
from ._wynn_ratelimit_handler import WynnRatelimitHandler
from .endpoint import GuildEndpoint, PlayerEndpoint

if TYPE_CHECKING:
    from .. import BaseRatelimitHandler


class WynnApi:

    def __init__(self) -> None:
        self._ratelimit = WynnRatelimitHandler(5, 180)
        self._request = HttpRequest(
            "https://beta-api.wynncraft.com",
            ratelimit=self.ratelimit,
            headers={"User-Agent": f"faz-db", "Content-Type": "application/json"
        })

        self._guild_endpoint = GuildEndpoint(self.request, 3, True)
        self._player_endpoint = PlayerEndpoint(self.request, 3, True)

    async def start(self) -> None:
        await self.request.start()

    async def close(self) -> None:
        await self.request.close()

    @property
    def guild(self) -> GuildEndpoint:
        return self._guild_endpoint

    @property
    def player(self) -> PlayerEndpoint:
        return self._player_endpoint

    @property
    def ratelimit(self) -> BaseRatelimitHandler:
        return self._ratelimit

    @property
    def request(self) -> HttpRequest:
        return self._request

    async def __aenter__(self) -> WynnApi:
        await self.request.__aenter__()
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        await self.request.__aexit__(exc_type, exc, tb)
