from typing import TypedDict


PlayerActivityT = TypedDict("PlayerActivity", {
    "logoff_timestamp": int,  # NOTE: int unsigned
    "logon_timestamp": int,  # NOTE: int unsigned
    "uuid": bytes  # NOTE: binary(16)
})
