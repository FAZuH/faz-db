from typing import Dict, TypeAlias, TypedDict


Server: TypeAlias = str
UsernameOrUUID: TypeAlias = str


OnlinePlayerList = TypedDict("OnlinePlayerList", {
    "total": int,
    "players": Dict[UsernameOrUUID, Server]
})