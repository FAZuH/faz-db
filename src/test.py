import asyncio
from request.mojang_request import MojangRequest
from request.wynncraft_request import WynncraftRequest


async def main():
    req = MojangRequest()
    resp = await req.get_uuids(["FAZuH", "Salted", "Jumla"])
    print(resp)
    return

asyncio.run(main())
