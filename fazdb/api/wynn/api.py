from __future__ import annotations
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from .endpoint import GuildEndpoint, PlayerEndpoint
    from .. import HttpRequest, RatelimitHandler


class Api(Protocol):
    """<<interface>>"""
    async def start(self) -> None: ...
    async def close(self) -> None: ...
    @property
    def guild(self) -> GuildEndpoint: ...
    @property
    def player(self) -> PlayerEndpoint: ...
    @property
    def ratelimit(self) -> RatelimitHandler: ...
    @property
    def request(self) -> HttpRequest: ...
    async def __aenter__(self) -> Api: ...
    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any): ...
