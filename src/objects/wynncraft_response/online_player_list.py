from typing import Dict, TypeAlias, TypedDict


Server: TypeAlias = str
Username: TypeAlias = str


OnlinePlayerList = TypedDict("OnlinePlayerList", {
    "total": int,
    "players": Dict[Username, Server]
})