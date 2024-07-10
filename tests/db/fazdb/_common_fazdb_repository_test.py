from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING

from fazdb.db.fazdb import FazdbDatabase

from .._common_db_repository_test import CommonDbRepositoryTest

if TYPE_CHECKING:
    from fazdb.db import BaseRepository


class CommonFazdbRepositoryTest:

    class Test[R: BaseRepository](CommonDbRepositoryTest.Test[FazdbDatabase, R], ABC):

        # override
        @property
        def database_type(self) -> type[FazdbDatabase]:
            return FazdbDatabase
