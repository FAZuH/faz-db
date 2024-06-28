from __future__ import annotations
import asyncio
from time import sleep

from fazdb.app import FazDb


class Main:

    app = FazDb()

    @classmethod
    def main(cls) -> None:
        cls.app.start()
        while True:  # keep-alive
            sleep(69_420)


if __name__ == "__main__":
    try:
        Main.main()
    except Exception as e:
        logger = Main.app.logger
        logger.console.exception(str(e))
        asyncio.run(logger.discord.error(f"FATAL ERROR", e))
        exit(1)
