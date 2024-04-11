from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING, Any

from aiohttp import ClientSession, ClientTimeout

from . import ResponseSet
from wynndb import (
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

if TYPE_CHECKING:
    from aiohttp import ClientResponse
    from . import RatelimitHandler


class HttpRequest:

    def __init__(
        self,
        base_url: str,
        api_key: None | str = None,
        headers: dict[str, Any] = {},
        ratelimit: None | RatelimitHandler = None,
        timeout: int = 120
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url
        self._ratelimit = ratelimit
        self._headers = headers
        self._timeout = timeout

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
            retries: None | int = None,  # HACK: bad code obv. please change this if you know a better
            retry_on_exc: bool = False
        ) -> ResponseSet[Any, Any]:
        if retry_on_exc and retries is None:
            raise ValueError("Retries must be set to a valid integer if retry_on_exc is True")

        if self._session is None or self._session.closed:
            raise KansError("Session is not open")

        resp: ClientResponse
        if self._ratelimit:
            await self._ratelimit.limit()

        resp = await self._session.get(url_param)

        if resp.ok:
            if self._ratelimit:
                self._ratelimit.update(dict(resp.headers))
            return ResponseSet(await resp.json(), dict(resp.headers))

        try:
            match resp.status:
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

        except HTTPError as e:
            if retry_on_exc and retries is not None:
                if retries <= 0:
                    raise TooManyRetries(url_param + f" ({e})")
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
