from asyncio import gather
from vindicator import (
    Fetch,
    FetchGuild,
    FetchOnline,
    FetchPlayer,
    WynncraftRequest
)
from vindicator.constants import *
from vindicator.typehints import *


class Fetcher:
    """Base class that manages request loop and dbquery loop for all Fetch objects"""

    def __init__(self) -> None:
        self._concurrent_request: int = 25
        self._wynncraft_request: WynncraftRequest = WynncraftRequest()
        self._fetch_guild: Fetch = FetchGuild(self._wynncraft_request)  # 2
        self._fetch_online: Fetch = FetchOnline(self._wynncraft_request)  # 1
        self._fetch_player: Fetch = FetchPlayer(self._wynncraft_request)  # 3
        self._running_request_queue: List[Coro[None]] = []
        return

    async def do_requests(self) -> None:
        """Called every 5 seconds. For every call:
        1. Checks if _running_request_queue is empty.
        2. If empty. Fills it with 25 request coroutines from all Fetch object queue with lowest timestamp,
        and runs all 25 concurrently.
        3. If not empty. return."""
        # fetch_online_requests: Dict[float, Coro[None]] = self._fetch_online.dequeue_requests()
        # fetch_player_requests: Dict[float, Coro[None]] = self._fetch_player.dequeue_requests()
        # fetch_guild_requests: Dict[float, Coro[None]] = self._fetch_guild.dequeue_requests()
        # requests: Dict[float, Coro[None]] = fetch_online_requests | fetch_player_requests |

        # coros: List[Coro[None]] = []
        # for _ in range(concurrent_request):
        #     if requests:
        #         # Dequeue the request with the lowest timestamp
        #         coros.append(requests.pop(min(requests.keys())))
        #     else:
        #         break

        if not self._running_request_queue:
            guild_request_queue: Dict[float, Coro[None]] = self._fetch_guild.get_request_queue()
            online_request_queue: Dict[float, Coro[None]] = self._fetch_online.get_request_queue()
            player_request_queue: Dict[float, Coro[None]] = self._fetch_player.get_request_queue()
            temp_placeholder = []
            # get 25 request coroutines from all Fetch object queue with lowest timestamp
            # TODO: bad design, change later
            for _ in range(self._concurrent_request):
                if guild_request_queue:
                    temp_placeholder.append(guild_request_queue.pop(min(guild_request_queue.keys())))
                elif online_request_queue:
                    temp_placeholder.append(online_request_queue.pop(min(online_request_queue.keys())))
                elif player_request_queue:
                    temp_placeholder.append(player_request_queue.pop(min(player_request_queue.keys())))
                else:
                    break

        # Opens session so that Fetch objects can use it. Bad design ik
        # TODO: Improve design
        async with self._wynncraft_request:
            # TODO: catch and log exceptions
            await gather(*self._running_request_queue, return_exceptions=True)
            self._running_request_queue.clear()
        return

    # TODO:
    def do_dbwrite(self) -> None:
        return

    # TODO:
    def process_responses(self) -> None:
        return

    # TODO: loop this mf
    async def run(self) -> None:
        self._fetch_online.run()
        self._fetch_player.run()
        self._fetch_guild.run()
        await self.do_requests()
        self.process_responses()
        self.do_dbwrite()
        return
