from __future__ import annotations

from kans import Kans


class Main:

    @staticmethod
    def main() -> None:
        kans = Kans()
        kans.start()
        while True:
            inp = input("")
            if inp == "exit":
                kans.heartbeat.stop()
                exit(0)


if __name__ == "__main__":
    Main.main()
