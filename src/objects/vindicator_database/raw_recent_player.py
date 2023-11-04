from typing import TypedDict, Union


class RawRecentPlayer(TypedDict):
    response: Union[dict, list]  # NOTE: json
    timestamp: int  # NOTE: int unsigned
    uuid: bytes  # NOTE: binary(16)
