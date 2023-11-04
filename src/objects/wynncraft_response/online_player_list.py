from typing import Dict, TypedDict


Username = Server = str

OnlinePlayerList = TypedDict("OnlinePlayerList", {
    "total": int,
    "players": Dict[Username, Server]
})