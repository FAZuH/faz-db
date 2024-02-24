from __future__ import annotations
from time import sleep

from kans.app import Kans


class Main:

    @staticmethod
    def main() -> None:
        kans = Kans()
        kans.start()

        while True:
            inp = input()
            if inp == "exit":
                kans.stop()
                exit(0)
            sleep(1)


if __name__ == "__main__":
    Main.main()
