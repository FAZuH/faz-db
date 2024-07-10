from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .base_async_database import BaseAsyncDatabase
    from .base_model import BaseModel
    from .base_repository import BaseRepository
from .fazdb import FazdbDatabase
