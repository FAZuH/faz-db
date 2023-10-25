from typing import TypedDict, Union


class RawLatestOthers(TypedDict):
    endpoint: str  # NOTE: enum('guild_list', 'territory_list', 'online_player_list')
    response: Union[dict, list]  # NOTE: json
