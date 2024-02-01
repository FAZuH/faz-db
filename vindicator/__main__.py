from __future__ import annotations
import asyncio
from traceback import format_exception
from typing import TYPE_CHECKING

from vindicator import FetchCore, VindicatorWebhook

if TYPE_CHECKING:
    from asyncio import Task


class Main:

    @staticmethod
    async def main() -> None:
        fetch_core: Task[None] = asyncio.create_task(FetchCore().start())
        await asyncio.sleep(1.0)

        while True:
            try:
                if fetch_core.done() and fetch_core.exception():
                    await fetch_core
                await asyncio.sleep(1.0)
            except Exception as e:
                await VindicatorWebhook.send(
                    "error", "error", "Fatal error occured on Main.main(). Program has stopped\n"
                    f"```{''.join(format_exception(e))}```"
                )
                raise


# from vindicator import WynnApi
# class Test:
#     @staticmethod
#     async def main():
#         api = WynnApi()
#         async with api:
#             avo = await api.get_guild_stats('Avicia')
#             assert avo.body.name == 'Avicia'
#         return


if __name__ == "__main__":
    asyncio.run(Main.main())
