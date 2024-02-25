from datetime import datetime as dt
from dateutil import parser

from . import DateField


class HeaderDateField(DateField):

    HEADERS_DATEFMT: str = "%a, %d %b %Y %H:%M:%S %Z"

    def __init__(self, datestr: str) -> None:
        super().__init__(datestr, self.HEADERS_DATEFMT)

    def to_datetime(self) -> dt:
        return parser.parse(self.datestr)
