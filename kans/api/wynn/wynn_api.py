from __future__ import annotations
from typing import Any, TYPE_CHECKING

from kans import (
    __version__,
    GuildResponse,
    HttpRequest,
    PlayerResponse,
    PlayersResponse,
    ResponseSet,
    Ratelimit,
)

if TYPE_CHECKING:
    from uuid import UUID
    from kans import ResponseSet



class WynnApi:

    def __init__(self) -> None:
        self._request: HttpRequest = HttpRequest("https://api.wynncraft.com", ratelimit=Ratelimit(180, 60), headers={
            "User-Agent": f"Vindicator/{__version__}",
            "Content-Type": "application/json"
        })

    async def start(self) -> None:
        await self._request.start()

    async def close(self) -> None:
        await self._request.close()

    async def __aenter__(self) -> WynnApi:
        await self._request.__aenter__()
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        await self._request.__aexit__(exc_type, exc, tb)

    async def get_guild_stats(self, name_or_prefix: str, is_prefix: bool = False) -> GuildResponse:
        response: ResponseSet[Any, Any] = await self._request.get(
                f"/v3/guild/{'prefix/' if is_prefix else ''}{name_or_prefix}",
                retries=3,
                retry_on_exc=True
        )
        return GuildResponse(response.body, response.headers)

    async def get_online_uuids(self) -> PlayersResponse:
        response: ResponseSet[Any, Any] = await self._request.get(
                "/v3/player?identifier=uuid",
                retries=3,
                retry_on_exc=True
        )
        return PlayersResponse(response.body, response.headers)

    async def get_player_stats(self, username_or_uuid: str | UUID) -> PlayerResponse:
        response: ResponseSet[Any, Any] = await self._request.get(
                f"/v3/player/{username_or_uuid}?fullResult=True",
                retries=3,
                retry_on_exc=True
        )
        return PlayerResponse(response.body, response.headers)
