from typing import Any

from ...base_response import BaseResponse
from ..model import Headers, Player


class PlayerResponse(BaseResponse[Player, Headers]):

    def __init__(self, body: dict[str, Any], headers: dict[str, Any]) -> None:
        super().__init__(Player(body), Headers(headers))

    # override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(username={self.body.username})"
