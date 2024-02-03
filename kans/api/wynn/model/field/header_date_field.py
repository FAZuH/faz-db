from src import DateField


class HeaderDateField(DateField):

    HEADERS_DATEFMT: str = "%a, %d %b %Y %H:%M:%S %Z"

    def __init__(self, datestr: str) -> None:
        super().__init__(datestr, self.HEADERS_DATEFMT)
