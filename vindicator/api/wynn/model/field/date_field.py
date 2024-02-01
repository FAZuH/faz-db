from datetime import datetime as dt


class DateField:

    def __init__(self, datestr: str, datefmt: str) -> None:
        self._datestr: str = datestr
        self._datefmt: str = datefmt

    def __str__(self) -> str:
        return self.datestr

    def to_datetime(self) -> dt:
        return dt.strptime(self.datestr, self.datefmt)

    @property
    def datestr(self) -> str:
        return self._datestr

    @property
    def datefmt(self) -> str:
        return self._datefmt
