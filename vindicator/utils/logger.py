from __future__ import annotations
import asyncio
from asyncio import create_task
from functools import wraps
from inspect import iscoroutinefunction
from time import perf_counter

from loguru import logger

from vindicator.typehints import *

T = TypeVar("T")
P = ParamSpec("P")


def _getclsatr(cls, attr) -> Any:
    return getattr(cls, attr, "error in accessing class property")


class Logger:

    _is_disabled: bool = False

    @classmethod
    async def disable(cls, seconds: float) -> None:
        cls._is_disabled = True
        await asyncio.sleep(seconds)
        cls._is_disabled = False

    @classmethod
    def logging_decorator(cls, f: Callable[P, T]) -> Callable[P, Coroutine[Any, Any, T]]:
        @wraps(f)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            t0: float = perf_counter()
            result = (await f(*args, **kwargs)) if iscoroutinefunction(f) else f(*args, **kwargs)
            if not cls._is_disabled:
                try:
                    Logger._send_log(f.__qualname__, f"{perf_counter() - t0:.2f}")
                except Exception as e:
                    logger.error(f"Failed to send log for {f.__qualname__}: {e}")
                    create_task(cls.disable(300))
            return result
        return wrapper

    @staticmethod
    def _send_log(fname: str, td: str) -> None:
        from vindicator import VindicatorWebhook, FetchOnline, FetchPlayer, FetchGuild
        match fname:
            case "FetchOnline._run":
                create_task(VindicatorWebhook.log("fetch_online", "success", {
                    "logged off": len(_getclsatr(FetchOnline, "_logged_off")),
                    "logged on": len(_getclsatr(FetchOnline, "_logged_on")),
                    "online": _getclsatr(FetchOnline, "_raw_online_uuids")["total"],
                    "time spent": td
                }, title="FetchOnline loop finished"))
            case "FetchPlayer._run":
                create_task(VindicatorWebhook.log("fetch_player", "success", {
                    "fetched players": len(_getclsatr(FetchPlayer, "_latest_fetch")),
                    "time spent": td
                }, title="FetchPlayer loop finished"))
            case "FetchGuild._run":
                create_task(VindicatorWebhook.log("fetch_guild", "success", {
                    "fetched guilds": len(_getclsatr(FetchGuild, "_latest_fetch")),
                    "time spent": td
                }, title="FetchGuild loop finished"))
            case "FetchOnline._request_api":
                create_task(VindicatorWebhook.log("wynncraft_request", "request", {
                    "endpoint": "onlinePlayers",
                    "online": _getclsatr(FetchOnline, "_raw_online_uuids")["total"],
                    "time spent": td
                }, title="Request online players"))
            case "PlayerServerUtil.to_db":
                create_task(VindicatorWebhook.log("database", "update", {
                    "table": "player_main_info",
                    "time spent": td
                }, title="Save players' servers"))
            case "PlayerActivityUtil.to_db":
                create_task(VindicatorWebhook.log("database", "write", {
                    "table": "player_activity",
                    "time spent": td
                }, title="Save player activities"))
            case "FetchPlayer._fetch_players":
                create_task(VindicatorWebhook.log("wynncraft_request", "request", {
                    "fetched players": len(_getclsatr(FetchPlayer, "_latest_fetch")),
                    "time spent": td,
                }, title="Request player stats"))
            case "FetchPlayer._to_db":
                create_task(VindicatorWebhook.log("database", "write", {
                    "records": len(_getclsatr(FetchPlayer, "_latest_fetch")),
                    "time spent": td,
                }, title="Save fetched players"))
            case "FetchGuild._fetch_guilds":
                create_task(VindicatorWebhook.log("wynncraft_request", "request", {
                    "fetched guilds": len(_getclsatr(FetchGuild, "_latest_fetch")),
                    "time spent": td,
                }, title="Request guild stats"))
            case "FetchGuild._to_db":
                create_task(VindicatorWebhook.log("database", "write", {
                    "records": len(_getclsatr(FetchGuild, "_latest_fetch")),
                    "time spent": td,
                }, title="Save fetched guilds"))
            case _:
                print(f"Logger: Function/method {fname} doesn't match any cases")

