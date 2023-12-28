from __future__ import annotations
import asyncio
from traceback import format_exception
from typing import TYPE_CHECKING

from vindicator import FetchGuild, FetchOnline, FetchPlayer, VindicatorWebhook

if TYPE_CHECKING:
    from asyncio import Task


class Main:

    @staticmethod
    async def main() -> None:
        from time import time
        t0 = time()
        fetch_online_task: Task = FetchOnline().run.start(); await asyncio.sleep(10.0)
        fetch_player_task: Task = FetchPlayer().run.start(); await asyncio.sleep(10.0)
        fetch_guild_task: Task = FetchGuild().run.start(); await asyncio.sleep(10.0)
        fetch_online_task.set_name("FetchOnline")
        fetch_player_task.set_name("FetchPlayer")
        fetch_guild_task.set_name("FetchGuild")

        while True:
            # if time() > t0 + 3600.0:
            #     from loguru import logger
            #     logger.success("Exiting program")
            #     exit(0)
            try:
                if fetch_online_task.done() and fetch_online_task.exception():
                    await fetch_online_task
                if fetch_player_task.done() and fetch_player_task.exception():
                    await fetch_player_task
                if fetch_guild_task.done() and fetch_guild_task.exception():
                    await fetch_guild_task
                await asyncio.sleep(10.0)
            except Exception as e:
                await VindicatorWebhook.send(
                    "error", "error", "Fatal error occured on Main.main(). Program has stopped\n"
                    f"```{''.join(format_exception(e))}```"
                )
                raise


# class Test:

#     @staticmethod
#     async def main() -> None:
#         from time import perf_counter
#         print('start')
#         t0=perf_counter(); await Test.test(); t1=perf_counter()
#         print('stop, elapsed', f"{t1-t0:.2f}")

#     from vindicator.utils.error_handler import ErrorHandler
#     @staticmethod
#     @ErrorHandler.aretry(times=3, exceptions=Exception)
#     async def test() -> None:
#         from vindicator import WynncraftRequest
#         async with WynncraftRequest._rm.session as s:
#             resp = await WynncraftRequest.get_player_stats_coro(s, "ee24ee2c-7f01-4f65-b598-5c67cd3f97e5")


if __name__ == "__main__":
    asyncio.run(Main.main())
