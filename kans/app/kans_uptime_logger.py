from kans import Database


class KansUptimeLogger:

    def __init__(self, db: Database):
        self._db = db
