from typing import TypedDict, Union


class RawResponses(TypedDict):
    endpoint: str  # NOTE: enum('guild_list', 'territory_list', 'online_player_list')
    response: dict  # NOTE: json
