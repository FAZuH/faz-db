from kans import Endpoint, GuildResponse


class GuildEndpoint(Endpoint):

    _PATH = "/v3/guild/%s%s"

    async def get(self, name_or_prefix: str, is_prefix: bool = False) -> GuildResponse:
        response = await self._request.get(
                self._PATH % (
                        "prefix/" if is_prefix else '',
                        name_or_prefix
                ),
                retries=self._retries,
                retry_on_exc=self._retry_on_exc,
        )
        return GuildResponse(response.body, response.headers)
