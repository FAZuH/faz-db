from __future__ import annotations
from typing import TYPE_CHECKING

from kans import Endpoint, PlayerResponse

if TYPE_CHECKING:
    from uuid import UUID


class PlayerEndpoint(Endpoint):

    _PATH = "/v3/player/%s?fullResult=True"

    async def get(self, username_or_uuid: str | UUID) -> PlayerResponse:
        response = await self._request.get(
                self._PATH % username_or_uuid,
                retries=self._retries,
                retry_on_exc=self._retry_on_exc,
        )
        return PlayerResponse(response.body, response.headers)
