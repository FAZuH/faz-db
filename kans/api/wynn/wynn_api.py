from __future__ import annotations
from typing import TYPE_CHECKING, Any

from . import Api
from .endpoint import GuildEndpoint, PlayerEndpoint
from kans import __version__
from kans.util import HttpRequest, Ratelimit

if TYPE_CHECKING:
    from loguru import Logger


class WynnApi(Api):

    def __init__(self, logger: Logger) -> None:
        self._ratelimit = Ratelimit(180, 60, logger)
        self._request: HttpRequest = HttpRequest(
                "https://api.wynncraft.com",
                ratelimit=self._ratelimit,
                headers={"User-Agent": f"Kans/{__version__}", "Content-Type": "application/json"
        })

    def start(self) -> None:
        self._request.start()

    async def close(self) -> None:
        await self._request.close()

    @property
    def guild(self) -> GuildEndpoint:
        return GuildEndpoint(self._request, 3, True)

    @property
    def player(self) -> PlayerEndpoint:
        return PlayerEndpoint(self._request, 3, True)

    @property
    def ratelimit(self) -> Ratelimit:
        return self._ratelimit

    @property
    def request(self) -> HttpRequest:
        return self._request

    async def __aenter__(self) -> Api:
        await self._request.__aenter__()
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        await self._request.__aexit__(exc_type, exc, tb)
