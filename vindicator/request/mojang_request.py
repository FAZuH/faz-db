from __future__ import annotations
from typing import TYPE_CHECKING, List, Union
from uuid import UUID

from .request_base import RequestBase
from .ratelimit import Ratelimit
from errors import VindicatorError

if TYPE_CHECKING:
    from aiohttp import ClientResponse


class MojangRequest(RequestBase):

    mojang_rl: Ratelimit = Ratelimit(60, 60)

    def __init__(self) -> None:
        super().__init__("https://api.mojang.com")

    async def __aenter__(self) -> MojangRequest:
        return self

    async def __atexit__(self) -> None:
        await self._close()

    async def get_uuids(self, uuids: List[str]) -> dict:
        url_param: str = "/profiles/minecraft"
        resp: "ClientResponse" = await self.post(url_param, uuids)

        data = await resp.json()

        if not isinstance(data, list):
            raise VindicatorError

        return {name_data["name"]: name_data["id"] for name_data in data}  # type: ignore
