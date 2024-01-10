from vindicator import DatabaseBase


class WynncraftDataDatabase(DatabaseBase):
    _DATABASE: str = "wynncraft_data"
    _PASSWORD: str = "root"
    _RETRIES: int = 2
    _USER: str = "root"
