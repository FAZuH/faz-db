from __future__ import annotations
from abc import ABC
from decimal import Decimal
from typing import Any, Iterable, TYPE_CHECKING

from sqlalchemy import Column, Tuple, exists, select, text, tuple_
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.schema import CreateTable

if TYPE_CHECKING:
    from sqlalchemy import Table
    from sqlalchemy.ext.asyncio import AsyncSession
    from .base_async_database import BaseAsyncDatabase
    from .base_model import BaseModel


class BaseRepository[T: BaseModel, ID](ABC):

    def __init__(self, database: BaseAsyncDatabase, model_cls: type[T]) -> None:
        self._database = database
        self._model_cls = model_cls

    async def table_disk_usage(self, *, session: None | AsyncSession = None) -> Decimal:
        """Calculate the size of the table in bytes.

        Parameters
        ----------
        conn : AsyncSession, optional
            Optional AsyncSession object to use for the database connection.
            If not provided, a new session will be created.

        Returns
        -------
        Decimal
            Size of the table in bytes.
        """
        SQL = f"""
            SELECT
                ROUND(((data_length + index_length)), 2) AS "size_bytes"
            FROM
                information_schema.TABLES
            WHERE
                table_schema = :schema
                AND table_name = :table_name;
        """
        params = {
            "schema": self._database.engine.url.database,
            "table_name": self.table_name
        }

        async with self._database.must_enter_session(session) as session:
            result = await session.execute(text(SQL), params)

        row = result.fetchone()
        ret = Decimal(row["size_bytes"]) if (row and row["size_bytes"] is not None) else Decimal(0)  # type: ignore
        return ret

    async def create_table(self, *, session: None | AsyncSession = None) -> None:
        """Create the table associated with the repository if it does not already exist.

        Parameters
        ----------
        session : AsyncSession, optional
            Optional AsyncSession object to use for the database connection.
            If not provided, a new session will be created.
        """
        stmt = CreateTable(self.table, if_not_exists=True)
        async with self.database.must_enter_session(session) as session:
            await session.execute(stmt)

    async def insert(
        self,
        entity: Iterable[T] | T,
        *,
        session: None | AsyncSession = None,
        ignore_on_duplicate: bool = False,
        replace_on_duplicate: bool = False,
        columns_to_replace: Iterable[str] | None = None
    ) -> None:
        """Insert one or more entities into the database.

        Parameters
        ----------
        entity : Iterable[T] | T
            An entity or an iterable of entities to be inserted into the database.
        session : AsyncSession, optional
            Optional AsyncSession object to use for the database connection.
            If not provided, a new session will be created.
        """
        if ignore_on_duplicate and replace_on_duplicate:
            raise ValueError("ignore_on_duplicate and replace_on_duplicate cannot be both True")

        entities = self._ensure_iterable(entity)
        table = self.get_model_cls().get_table()
        entity_d = [dict(e.items(trim_end_underscore=True)) for e in entities]
        stmt = insert(table).values(entity_d)

        if replace_on_duplicate:
            if columns_to_replace is None:
                columns_to_replace = [c.name for c in table.columns if not c.primary_key]
            stmt = stmt.on_duplicate_key_update(**{c: getattr(stmt.inserted, c) for c in columns_to_replace})

        if ignore_on_duplicate:
            stmt = stmt.prefix_with("IGNORE")

        async with self.database.must_enter_session(session) as session:
            await session.execute(stmt)

    async def delete(self, id_: ID, *, session: AsyncSession | None = None) -> None:
        """Deletes an entry from the repository based on `id_`

        Parameters
        ----------
        id_: Any
            Primary_key value of the entry to delete.

        conn : AsyncSession, optional
            Optional AsyncSession object to use for the database connection.
            If not provided, a new session will be created.
        """
        primary_keys = self._get_primary_key()
        stmt = self.table.delete().where(primary_keys == id_)
        async with self.database.must_enter_session(session) as session:
            await session.execute(stmt)

    async def is_exists(self, id_: ID, *, session: None | AsyncSession = None) -> bool:
        """Check if an entry with the given primary key exists in the database.

        Parameters
        ----------
        id_ : ID
            Primary key value of the entry to check.
        session : AsyncSession, optional
            Optional AsyncSession object to use for the database connection.
            If not provided, a new session will be created.

        Returns
        -------
        bool
            True if the entry exists, False otherwise.
        """
        primary_keys = self._get_primary_key()
        stmt = select(exists().where(primary_keys == id_))
        async with self.database.must_enter_session(session) as session:
            result = await session.execute(stmt)

        is_exist = result.scalar()
        return is_exist or False

    async def truncate(self, *, session: None | AsyncSession = None) -> None:
        """Truncates the table.

        Parameters
        ----------
        session : AsyncSession, optional
            Optional AsyncSession object to use for the database connection.
            If not provided, a new session will be created.
        """
        model = self.get_model_cls()
        async with self.database.must_enter_session(session) as session:
            await session.execute(model.get_table().delete())

    def get_model_cls(self) -> type[T]:
        return self._model_cls

    @property
    def database(self) -> BaseAsyncDatabase:
        return self._database

    @property
    def model(self) -> type[T]:
        return self.get_model_cls()

    @property
    def table(self) -> Table:
        return self.model.get_table()

    @property
    def table_name(self) -> str:
        return self.model.__tablename__

    def _get_primary_key(self) -> Tuple[Column[Any], ...] | Column[Any]:
        model_cls = self.get_model_cls()
        primary_keys: tuple[Column[Any], ...] | Column[Any] = model_cls.__mapper__.primary_key

        if not isinstance(primary_keys, tuple):  # type: ignore
            return tuple_(primary_keys)

        if len(primary_keys) == 1:
            return primary_keys[0]

        return tuple_(*primary_keys)

    @staticmethod
    def _ensure_iterable[U](obj: Iterable[U] | U) -> Iterable[U]:
        if isinstance(obj, Iterable):
            return obj
        else:
            return [obj]

    def _convert_comparable(self, id_: Iterable[ID] | ID) -> list[tuple[ID, ...]]:
        ids = self._ensure_iterable(id_)
        ret = [(id__,) for id__ in ids]
        return ret

    def _to_dict(self, objs: Iterable[T]) -> list[dict[str, Any]]:
        return [
            {c.name: getattr(obj, c.name) for c in obj.get_table().columns}
            for obj in objs
        ]
