from typing import Any

from ...base_response import BaseResponse
from ..model import Guild, Headers


class GuildResponse(BaseResponse[Guild, Headers]):

    def __init__(self, body: dict[str, Any], headers: dict[str, Any]) -> None:
        super().__init__(Guild(body), Headers(headers))

    # override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(username={self.body.name})"
