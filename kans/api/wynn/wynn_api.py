from __future__ import annotations
from typing import TYPE_CHECKING, Any

from . import Api, WynnRatelimitHandler
from .endpoint import GuildEndpoint, PlayerEndpoint
from kans import __version__
from kans.util import HttpRequest, PerformanceRecorder

if TYPE_CHECKING:
    from loguru import Logger
    from kans.util import RatelimitHandler


class WynnApi(Api):

    def __init__(self, logger: Logger) -> None:
        self._perf = PerformanceRecorder()
        self._ratelimit = WynnRatelimitHandler(5, 180, logger)
        self._request: HttpRequest = HttpRequest(
                "https://api.wynncraft.com",
                ratelimit=self._ratelimit,
                headers={"User-Agent": f"Kans/{__version__}", "Content-Type": "application/json"
        })

        self._guild_endpoint = GuildEndpoint(self._request, 3, True)
        self._player_endpoint = PlayerEndpoint(self._request, 3, True)

        # HACK: this is a hacky way to do this, but it works for now
        self._guild_endpoint.get = self._perf.listen_async(self._guild_endpoint.get, "guild.get")
        self._guild_endpoint.get_from_prefix = self._perf.listen_async(self._guild_endpoint.get_from_prefix, "guild.get_from_prefix")
        self._player_endpoint.get_full_stats = self._perf.listen_async(self._player_endpoint.get_full_stats, "player.get_full_stats")
        self._player_endpoint.get_online_uuids = self._perf.listen_async(self._player_endpoint.get_online_uuids, "player.get_online_uuids")

    async def start(self) -> None:
        await self._request.start()

    async def close(self) -> None:
        await self._request.close()

    @property
    def guild(self) -> GuildEndpoint:
        return self._guild_endpoint

    @property
    def player(self) -> PlayerEndpoint:
        return self._player_endpoint

    @property
    def performance_recorder(self) -> PerformanceRecorder:
        return self._perf

    @property
    def ratelimit(self) -> RatelimitHandler:
        return self._ratelimit

    @property
    def request(self) -> HttpRequest:
        return self._request

    async def __aenter__(self) -> Api:
        await self._request.__aenter__()
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        await self._request.__aexit__(exc_type, exc, tb)
