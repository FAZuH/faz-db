from typing import TypedDict, Union


class RawOnlineGuild(TypedDict):
    guild_name: str  # NOTE: varchar(30)
    response: Union[dict, list]  # NOTE: json
