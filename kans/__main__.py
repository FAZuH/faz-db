from __future__ import annotations
import asyncio
from traceback import format_exception
from typing import TYPE_CHECKING

from src import FetchCore, VindicatorWebhook

if TYPE_CHECKING:
    from asyncio import Task


class Main:

    @staticmethod
    async def main() -> None:
        fetch_core: Task[None] = asyncio.create_task(FetchCore().start())

        while True:
            await asyncio.sleep(1.0)
            try:
                if fetch_core.done() and fetch_core.exception():
                    await fetch_core
            except Exception as e:
                await VindicatorWebhook.send(
                    "error", "error", "Fatal error occured on Main.main(). Program has stopped\n"
                    f"```{''.join(format_exception(e))}```"
                )
                raise


if __name__ == "__main__":
    asyncio.run(Main.main())
