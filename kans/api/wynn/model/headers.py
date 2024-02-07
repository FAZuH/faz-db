from datetime import datetime as dt
from datetime import timedelta as td
from typing import Any

from kans import HeaderDateField


class Headers:

    def __init__(self, raw: dict[str, Any]) -> None:
        self._raw: dict[str, Any] = raw
        self._cache_control: str = raw["Cache-Control"]
        self._date: HeaderDateField = HeaderDateField(raw["Date"])
        self._expires: HeaderDateField = HeaderDateField(raw["Expires"])
        self._ratelimit_limit: str = raw["RateLimit-Limit"]
        self._ratelimit_remaining: str = raw["RateLimit-Remaining"]
        self._ratelimit_reset: str = raw["RateLimit-Reset"]

    def get_expiry_datetime(self) -> dt:
        return self.expires.to_datetime()

    def get_expiry_timediff(self) -> td:
        return self.get_expiry_datetime() - dt.now()

    def get_datetime(self) -> dt:
        """
        Get the timestamp of the response.

        Returns:
            dt: The timestamp of the response.
        """
        expiry_date: dt = self.expires.to_datetime()
        cache_control: td = td(seconds=int(self.cache_control.split("=")[1]))
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
    def ratelimit_limit(self) -> str:
        return self._ratelimit_limit

    @property
    def ratelimit_remaining(self) -> str:
        return self._ratelimit_remaining

    @property
    def ratelimit_reset(self) -> str:
        return self._ratelimit_reset
