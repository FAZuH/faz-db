from __future__ import annotations
from decimal import Decimal
from typing import Any, Generator, TYPE_CHECKING, Self

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

if TYPE_CHECKING:
    from sqlalchemy.sql.schema import Table


class BaseModel(DeclarativeBase, AsyncAttrs):

    @classmethod
    def get_table(cls) -> Table:
        return cls.__table__  # type: ignore

    def clone(self) -> Self:
        return self.__class__(**dict(self.items()))

    def items(self) -> Generator[tuple[str, Any], None, None]:
        for k in self.get_table().columns:
            yield k.name, getattr(self, k.name)

    def __eq__(self, other: object) -> bool:
        for k, v in self.items():
            v_other = getattr(other, k)
            if v != v_other:
                return False
        return True

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __repr__(self) -> str:
        items = self.items()
        sorted_items = sorted(items, key=lambda x: x[0])
        params = ', '.join(f'{k}={self.__handle_repr_types(v)}' for k, v in sorted_items)
        return f"{self.__class__.__name__}({params})"

    @staticmethod
    def __handle_repr_types(obj: object):
        if isinstance(obj, Decimal):
            return float(obj)
        return obj
