from __future__ import annotations
import asyncio
from traceback import format_exception

from vindicator import FetchOnline, FetchPlayer, FetchGuild, VindicatorWebhook
from vindicator.typehints import *


class Main:

    @staticmethod
    async def main() -> None:
        fetch_online_task: Task = FetchOnline.run.start(); await asyncio.sleep(10.0)
        fetch_player_task: Task = FetchPlayer.run.start(); await asyncio.sleep(10.0)
        fetch_guild_task: Task = FetchGuild.run.start(); await asyncio.sleep(10.0)

        while True:
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


if __name__ == "__main__":
    asyncio.run(Main.main())
