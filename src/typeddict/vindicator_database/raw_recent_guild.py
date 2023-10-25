from typing import TypedDict, Union


class RawRecentGuild(TypedDict):
    guild_name: str  # NOTE: varchar(30)
    response: Union[dict, list]  # NOTE: json
    timestamp: int  # NOTE: int unsigned
