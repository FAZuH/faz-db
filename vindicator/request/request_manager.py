from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING, Dict, Optional

from aiohttp import ClientSession, ClientTimeout

from vindicator import (
    __version__,
    BadRequest,
    Forbidden,
    HTTPError,
    NotFound,
    ServerError,
    TooManyRequests,
    Unauthorized,
    VindicatorError,
    VindicatorWebhook
)

if TYPE_CHECKING:
    from vindicator.types import *

class RequestManager:

    def __init__(self, base_url: str, api_key: Optional[str] = None, ratelimit: Optional[Ratelimit] = None, timeout: int = 120) -> None:
        self._api_key: Optional[str] = api_key
        self._base_url: str = base_url
        self._ratelimit: Optional[Ratelimit] = ratelimit
        self._headers: Dict[str, str] = {
            "User-Agent": f"Vindicator/{__version__}",
            "Content-Type": "application/json"
        }
        self._timeout: int = timeout

        if self._api_key is not None:
            self._headers["apikey"] = self._api_key

    @property
    def session(self) -> ClientSession:
        return ClientSession(self._base_url, headers=self._headers, timeout=ClientTimeout(self._timeout))

    async def get(
            self,
            url_param: str,
            session: ClientSession,
            retries: int = -10,
            retry_on_exc: bool = False
        ) -> ClientResponse:
        if retry_on_exc:
            if retries == -10:
                raise VindicatorError("Retries must be set if retry_on_exc is True")
            # elif retries <= 0:
            #     raise HTTPError("Exceeded max retries")

        if session.closed:
            raise VindicatorError("Session is closed")

        response: ClientResponse
        if self._ratelimit:
            await self._ratelimit.limit()
            response = await session.get(url_param)
            self._ratelimit.update(dict(response.headers))
        else:
            response = await session.get(url_param)

        try:
            if response.ok:
                return response

            if response.status == 400:
                raise BadRequest(url_param)

            if response.status == 401:
                raise Unauthorized(url_param)

            if response.status == 403:
                raise Forbidden(url_param)

            if response.status == 404:
                raise NotFound(url_param)

            if response.status == 429:
                raise TooManyRequests(url_param)

            if response.status >= 500:
                raise ServerError(url_param)

            raise VindicatorError(url_param)

        except HTTPError:
            if retry_on_exc:
                if retries <= 0:
                    await VindicatorWebhook.log("error", "error", {"url": url_param},
                        title=f"HTTPError: {response.status} - {response.reason}")
                    raise

                if response.status == 429:
                    if self._ratelimit:
                        await self._ratelimit.ratelimited()
                    else:
                        await asyncio.sleep(60)

                return await self.get(url_param, session, retries - 1, retry_on_exc)
            else:
                raise TooManyRequests(url_param)
