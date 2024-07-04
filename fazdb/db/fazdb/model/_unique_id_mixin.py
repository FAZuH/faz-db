import hashlib
from typing import Any

from . import BaseModel


class UniqueIdMixin(BaseModel):
    __abstract__ = True

    def __init__(self, **kw: Any):
        super().__init__(**kw)
        self.__compute_unique_id()
    
    def __compute_unique_id(self) -> None:
        columns = [str(getattr(self, col.name)) for col in self.get_table().columns if col.name != "unique_id"]
        to_hash = ''.join(columns).encode()
        hashed_columns = hashlib.sha256(to_hash).digest()
        self.unique_id = hashed_columns
