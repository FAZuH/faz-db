from typing import Any

from ..response import GuildResponse
from .base_endpoint import BaseEndpoint


class GuildEndpoint(BaseEndpoint):

    async def get(self, name: str) -> GuildResponse:
        return await self._get(f'{self.path}/{name}')

    async def get_from_prefix(self, prefix: str) -> GuildResponse:
        return await self._get(f"{self.path}/prefix/{prefix}")

    async def _get(self, *args: Any, **kwargs: Any) -> GuildResponse:
        response = await self._request.get(
                *args,
                **kwargs,
                retries=self._retries,
                retry_on_exc=self._retry_on_exc,
        )
        return GuildResponse(response.body, response.headers)

    # override
    @property
    def path(self) -> str:
        return "/v3/guild"
