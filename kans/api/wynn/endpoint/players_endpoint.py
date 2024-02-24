from . import AbstractEndpoint
from ..response import PlayersResponse


class PlayersEndpoint(AbstractEndpoint):

    _PATH = "/v3/player?identifier=uuid"

    async def get(self) -> PlayersResponse:
        response = await self._request.get(
                self._PATH,
                retries=self._retries,
                retry_on_exc=self._retry_on_exc,
        )
        return PlayersResponse(response.body, response.headers)
