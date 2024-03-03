from __future__ import annotations
import asyncio
from time import sleep
from typing import TYPE_CHECKING

from kans.app import Kans

if TYPE_CHECKING:
    from kans import App


class Main:

    def __init__(self) -> None:
        self._app = Kans()

    def main(self) -> None:
        self._app.start()

        while True:
            inp = input()
            if inp == "exit":
                self._app.stop()
                exit(0)
            sleep(0.1)

    @property
    def app(self) -> App:
        return self._app

if __name__ == "__main__":
    main = Main()
    try:
        main.main()
    except Exception as e:
        asyncio.run(main.app.logger.discord.error(f"FATAL ERROR", e))
        exit(1)
