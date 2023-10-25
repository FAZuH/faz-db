from typing import Dict, TypedDict


class OnlinePlayerList(TypedDict):
    onlinePlayers: int
    players: Dict[str, str]
