import asyncio
from vindicator.request.mojang_request import MojangRequest
from vindicator.request.wynncraft_request import WynncraftRequest


async def main():
    req = MojangRequest()
    resp = await req.get_uuids(["FAZuH", "Salted", "Jumla"])
    print(resp)
    return

asyncio.run(main())
