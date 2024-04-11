# The line `from typing import Any` is importing the `Any` type hint from the `typing` module in
# Python. The `Any` type hint is used to indicate that a variable can be of any type. It is often used
# when the specific type of a variable is not known or when a function can accept arguments of any
# type.
from typing import Any

from . import AbstractEndpoint
from ..response import GuildResponse


class GuildEndpoint(AbstractEndpoint):

    _PATH = "/v3/guild"

    async def get(self, name: str) -> GuildResponse:
        return await self._wrapped_get(f'{self.path}/{name}')

    async def get_from_prefix(self, prefix: str) -> GuildResponse:
        return await self._wrapped_get(f"{self.path}/prefix/{prefix}")

    async def _wrapped_get(self, *args: Any, **kwargs: Any) -> GuildResponse:
        response = await self._request.get(
                *args,
                **kwargs,
                retries=self._retries,
                retry_on_exc=self._retry_on_exc,
        )
        return GuildResponse(response.body, response.headers)

    @property
    def path(self) -> str:
        return self._PATH
