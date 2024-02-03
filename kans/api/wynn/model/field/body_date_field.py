from datetime import datetime as dt
from dateutil.tz import tzutc

from typing_extensions import override

from src import DateField


class BodyDateField(DateField):

    def __init__(self, datestr: str) -> None:
        super().__init__(datestr, "")

    @override
    def to_datetime(self) -> dt:
        return dt.strptime(self.datestr, "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=tzutc())
