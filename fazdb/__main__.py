from __future__ import annotations
from time import sleep

from loguru import logger

from fazdb.app import FazDb


class Main:

    app = FazDb()

    @classmethod
    def main(cls) -> None:
        cls.app.start()
        while True:  # keep-alive
            sleep(69_420)


if __name__ == "__main__":
    with logger.catch(level="CRITICAL"):
        Main.main()
