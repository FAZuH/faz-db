from typing import Optional, TypedDict


PlayerMainInfoT = TypedDict(("PlayerMainInfo"), {
    "first_join": Optional[int],  # int unsigned
    "latest_username": str,  # varchar(16)
    "server": Optional[str],  # varchar(10)
    "uuid": bytes,  # binary(16)
})
