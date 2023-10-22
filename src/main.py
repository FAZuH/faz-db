import asyncio

from request.request import Request


class Main:
    def __init__(self) -> None:
        pass

    def main(self) -> None:
        asyncio.run(self.start())

    async def start(self) -> None:
        await Request.start()


# if __name__ == "__main__":
#     Main().main()
