from __future__ import annotations
from typing import Any

from kans import (
    __version__,
    Api,
    GuildEndpoint,
    HttpRequest,
    PlayerEndpoint,
    PlayersEndpoint,
    Ratelimit,
)


class WynnApi(Api):

    def __init__(self) -> None:
        self._request: HttpRequest = HttpRequest(
                "https://api.wynncraft.com",
                ratelimit=Ratelimit(180, 60),
                headers={"User-Agent": f"Kans/{__version__}", "Content-Type": "application/json"
        })

    async def start(self) -> None:
        await self._request.start()

    async def close(self) -> None:
        await self._request.close()

    @property
    def guild(self) -> GuildEndpoint:
        return GuildEndpoint(self._request, 3, True)

    @property
    def players(self) -> PlayersEndpoint:
        return PlayersEndpoint(self._request, 3, True)

    @property
    def player(self) -> PlayerEndpoint:
        return PlayerEndpoint(self._request, 3, True)

    async def __aenter__(self) -> Api:
        await self._request.__aenter__()
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        await self._request.__aexit__(exc_type, exc, tb)
