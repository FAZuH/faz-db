from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING, Any

from aiohttp import ClientSession, ClientTimeout

from kans import (
    BadRequest,
    Forbidden,
    HTTPError,
    NotFound,
    Ratelimited,
    ServerError,
    TooManyRetries,
    Unauthorized,
    KansError
)
from kans.util import ResponseSet

if TYPE_CHECKING:
    from aiohttp import ClientResponse
    from kans.util import Ratelimit


class HttpRequest:

    def __init__(
        self,
        base_url: str,
        api_key: None | str = None,
        headers: dict[str, Any] = {},
        ratelimit: None | Ratelimit = None,
        timeout: int = 120
    ) -> None:
        self._api_key: None | str = api_key
        self._base_url: str = base_url
        self._ratelimit: None | Ratelimit = ratelimit
        self._headers: dict[str, str] = headers
        self._timeout: int = timeout

        if self._api_key is not None:
            self._headers["apikey"] = self._api_key
        self._session: None | ClientSession = None

    async def start(self) -> None:
        self._session = ClientSession(self._base_url, headers=self._headers, timeout=ClientTimeout(self._timeout))

    async def close(self) -> None:
        if self._session is not None:
            await self._session.close()

    async def get(
            self,
            url_param: str,
            retries: int = -69,
            retry_on_exc: bool = False
        ) -> ResponseSet[Any, Any]:
        if retry_on_exc:
            if retries == -69:
                raise ValueError("Retries must be set if retry_on_exc is True")

        if self._session is None or self._session.closed:
            raise KansError("Session is not open")

        response: ClientResponse
        if self._ratelimit:
            await self._ratelimit.limit()
            response = await self._session.get(url_param)
            self._ratelimit.update(dict(response.headers))
        else:
            response = await self._session.get(url_param)

        if response.ok:
            return ResponseSet(await response.json(), dict(response.headers))

        try:
            match response.status:
                case 400:
                    raise BadRequest(url_param)
                case 401:
                    raise Unauthorized(url_param)
                case 403:
                    raise Forbidden(url_param)
                case 404:
                    raise NotFound(url_param)
                case 429:
                    raise Ratelimited(url_param)
                case 500:
                    raise ServerError(url_param)
                case _:
                    raise HTTPError(url_param)

        except Ratelimited:
            if self._ratelimit:
                await self._ratelimit.ratelimited()
            else:
                await asyncio.sleep(60)
            return await self.get(url_param, retries, retry_on_exc)

        except HTTPError:
            if retry_on_exc is True:
                if retries <= 0:
                    # await VindicatorWebhook.log("error", "error", {"url": url_param},
                    #     title=f"HTTPError: {response.status} - {response.reason}")
                    raise TooManyRetries(url_param)
                return await self.get(url_param, retries - 1, retry_on_exc)
            raise

    def is_open(self) -> bool:
        return self._session is not None and not self._session.closed

    async def __aenter__(self) -> HttpRequest:
        await self.start()
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        if self._session is not None:
            await self._session.close()
