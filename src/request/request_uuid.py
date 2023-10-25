from .request_base import RequestBase

BASE_URL = "https://playerdb.co/api/player/minecraft"


class RequestMojang(RequestBase):
    def __init__(self) -> None:
        super().__init__(BASE_URL, timeout=60)

    async def get_uuid(self, uuid: str):
        url_parameters = f"/{uuid}"
        ret = await self.get(url_parameters)
        ret = await ret.json()
        return ret
