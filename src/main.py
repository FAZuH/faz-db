import asyncio

from request.fetch_online import FetchOnline
from request.fetch_player import FetchPlayer


class Main:

    @staticmethod
    async def main() -> None:
        fetch_online: FetchOnline = FetchOnline()
        fetch_player: FetchPlayer = FetchPlayer()

        t1: asyncio.Task = fetch_online.run.start()
        await asyncio.sleep(10.0)
        t2: asyncio.Task = fetch_player.loop_run.start()
        await asyncio.sleep(10.0)
        while True:
            try:
                if t1.done() and t1.exception():
                    await t1
                if t2.done() and t2.exception():
                    await t2
            except Exception as e:
                from webhook.vindicator_webhook import VindicatorWebhook
                from traceback import format_exception
                await VindicatorWebhook.send(
                    "error", "error", "Fatal error occured on Main.main. Program has been stopped\n"
                    f"{format_exception(e)}"
                )
                raise
            await asyncio.sleep(10.0)
        return


if __name__ == "__main__":
    asyncio.run(Main.main())
