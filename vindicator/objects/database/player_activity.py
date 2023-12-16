from typing import TypedDict


class PlayerActivity(TypedDict):
    logoff_timestamp: int  # NOTE: int unsigned
    logon_timestamp: int  # NOTE: int unsigned
    uuid: bytes  # NOTE: binary(16)
