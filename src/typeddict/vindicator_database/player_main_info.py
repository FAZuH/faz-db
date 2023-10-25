from typing import TypedDict, NotRequired


class PlayerMainInfo(TypedDict):
    first_join: NotRequired[int]  # NOTE: int unsigned
    latest_username: str  # NOTE: varchar(16)
    server: NotRequired[str]  # NOTE: varchar(10)
    timestamp: int  # NOTE: int unsigned
    uuid: bytes  # NOTE: binary(16)
