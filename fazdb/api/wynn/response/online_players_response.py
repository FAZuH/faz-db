from typing import Any

from ...base_response import BaseResponse
from ..model import Headers, OnlinePlayers


class OnlinePlayersResponse(BaseResponse[OnlinePlayers, Headers]):

    def __init__(self, body: dict[str, Any], headers: dict[str, Any]) -> None:
        super().__init__(OnlinePlayers(body), Headers(headers))
