from typing import TypedDict, Union


class RawOnlinePlayer(TypedDict):
    response: Union[dict, list]  # NOTE: json
    uuid: bytes  # NOTE: binary(16)
