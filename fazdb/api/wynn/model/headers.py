from datetime import datetime
from datetime import timedelta
from typing import Any

from .field import HeaderDateField


class Headers:

    def __init__(self, raw: dict[str, Any]) -> None:
        self._raw = raw
        self._cache_control = raw["Cache-Control"]
        self._date = HeaderDateField(raw["Date"])
        self._expires = HeaderDateField(raw["Expires"])
        self._ratelimit_limit = int(raw["RateLimit-Limit"])
        self._ratelimit_remaining = int(raw["RateLimit-Remaining"])
        self._ratelimit_reset = int(raw["RateLimit-Reset"])

    def to_datetime(self) -> datetime:
        """
        Get the timestamp of the response.

        Returns:
            datetime: The timestamp of the response.
        """
        expiry_date: datetime = self.expires.to_datetime()
        cache_control: timedelta = timedelta(seconds=int(self.cache_control.split("=")[1]))
        return expiry_date - cache_control

    @property
    def raw(self) -> dict[str, Any]:
        return self._raw

    @property
    def cache_control(self) -> str:
        return self._cache_control

    @property
    def date(self) -> HeaderDateField:
        return self._date

    @property
    def expires(self) -> HeaderDateField:
        return self._expires

    @property
    def ratelimit_limit(self) -> int:
        return self._ratelimit_limit

    @property
    def ratelimit_remaining(self) -> int:
        return self._ratelimit_remaining

    @property
    def ratelimit_reset(self) -> int:
        return self._ratelimit_reset
