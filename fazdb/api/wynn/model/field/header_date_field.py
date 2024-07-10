from datetime import datetime

from dateutil import parser

from ._date_field import DateField


class HeaderDateField(DateField):

    HEADERS_DATEFMT: str = "%a, %d %b %Y %H:%M:%S %Z"

    def __init__(self, datestr: str) -> None:
        super().__init__(datestr, self.HEADERS_DATEFMT)

    def to_datetime(self) -> datetime:
        return parser.parse(self.datestr)
