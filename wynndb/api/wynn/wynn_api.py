from __future__ import annotations
from typing import TYPE_CHECKING, Any

from . import Api, WynnRatelimitHandler
from .endpoint import GuildEndpoint, PlayerEndpoint
from wynndb import __version__
from .. import HttpRequest

if TYPE_CHECKING:
    from wynndb import Logger
    from .. import RatelimitHandler


class WynnApi(Api):

    def __init__(self, logger: Logger) -> None:
        self._logger = logger
        self._ratelimit = WynnRatelimitHandler(5, 180, self._logger)
        self._request = HttpRequest(
                "https://api.wynncraft.com",
                ratelimit=self._ratelimit,
                headers={"User-Agent": f"Kans/{__version__}", "Content-Type": "application/json"
        })

        self._guild_endpoint = GuildEndpoint(self._request, 3, True)
        self._player_endpoint = PlayerEndpoint(self._request, 3, True)

    async def start(self) -> None:
        await self._request.start()

    async def close(self) -> None:
        await self._request.close()

    @property
    def guild(self) -> GuildEndpoint:
        return self._guild_endpoint

    @property
    def player(self) -> PlayerEndpoint:
        return self._player_endpoint

    @property
    def ratelimit(self) -> RatelimitHandler:
        return self._ratelimit

    @property
    def request(self) -> HttpRequest:
        return self._request

    async def __aenter__(self) -> Api:
        await self._request.__aenter__()
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        await self._request.__aexit__(exc_type, exc, tb)