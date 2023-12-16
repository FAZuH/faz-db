from abc import ABC
import asyncio
from typing import TYPE_CHECKING, Dict, Optional, Union

import aiohttp
import asyncio_atexit

from constants import __version__
from errors import (
    BadRequest,
    Forbidden,
    NotFound,
    ServerError,
    TooManyRequests,
    Unauthorized,
    VindicatorError
)
from webhook.vindicator_webhook import VindicatorWebhook

if TYPE_CHECKING:
    from .ratelimit import Ratelimit

    from aiohttp import ClientResponse


class RequestBase(ABC):

    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: int = 120) -> None:
        self._api_key: Optional[str] = api_key

        headers: Dict[str, str] = {
            "User-Agent": f"Vindicator/{__version__}",
            "Content-Type": "application/json"
        }

        if self._api_key is not None:
            headers["apikey"] = self._api_key

        self._session = aiohttp.ClientSession(base_url, headers=headers, timeout=aiohttp.ClientTimeout(timeout))
        asyncio_atexit.register(self._close)

    async def _close(self) -> None:
        if not self._session.closed:
            await self._session.close()

    async def get(self, url_param: str, ratelimit: Optional["Ratelimit"] = None) -> "ClientResponse":
        if self._session.closed:
            raise RuntimeError("Client is closed.")

        if ratelimit is None:
            resp: "ClientResponse" = await self._session.get(url_param)
        else:
            await ratelimit.limit()
            ratelimit.update()
            resp: "ClientResponse" = await self._session.get(url_param)

        if resp.ok:
            return resp

        if resp.status == 400:
            raise BadRequest

        if resp.status == 401:
            raise Unauthorized

        if resp.status == 403:
            raise Forbidden

        if resp.status == 404:
            raise NotFound

        if resp.status == 429:
            if ratelimit:
                await ratelimit.ratelimited()
                return await self.get(url_param, ratelimit)

            asyncio.create_task(VindicatorWebhook.send("error", "error", f"Error {resp.status} - {resp.reason}"))
            raise TooManyRequests(f"{resp.status} - {resp.reason}")

        if resp.status >= 500:
            raise ServerError

        raise VindicatorError

    async def post(self, url_param: str, data: Union[dict, list], ratelimit: Optional["Ratelimit"] = None) -> "ClientResponse":
        resp: "ClientResponse" = await self._session.post(url_param, json=data)

        if resp.ok:
            return resp

        if resp.status == 400:
            raise BadRequest

        if resp.status == 401:
            raise Unauthorized

        if resp.status == 403:
            raise Forbidden

        if resp.status == 404:
            raise NotFound

        if resp.status == 429:
            if ratelimit:
                await ratelimit.ratelimited()
                return await self.get(url_param, ratelimit)

            asyncio.create_task(VindicatorWebhook.send("error", "error", f"Error {resp.status} - {resp.reason}"))
            raise TooManyRequests(f"{resp.status} - {resp.reason}")

        if resp.status >= 500:
            raise ServerError

        raise VindicatorError
