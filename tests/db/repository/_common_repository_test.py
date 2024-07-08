from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Sequence, TYPE_CHECKING
import unittest

from loguru import logger
from sqlalchemy import inspect, select

from fazdb.app import Config
from fazdb.db import fazdb

if TYPE_CHECKING:
    from sqlalchemy import Connection
    from fazdb.db.fazdb.model import BaseModel
    from fazdb.db.fazdb.repository._repository import Repository


class CommonRepositoryTest:

    # Nesting test classes like this prevents CommonRepositoryTest.Test from being run by unittest.
    class Test[T: BaseModel, ID](unittest.IsolatedAsyncioTestCase, ABC):

        # override
        async def asyncSetUp(self) -> None:
            Config.read()
            
            self.database = fazdb.FazdbDatabase(
                "mysql+aiomysql",
                Config.mysql_username,
                Config.mysql_password,
                Config.mysql_host,
                Config.mysql_port,
                "faz-db_test"
            )
            async with self.database.enter_session() as session:
                await self._repo.create_table(session=session)
                await self._repo.truncate(session=session)

            return await super().asyncSetUp()

        async def test_create_table_successful(self) -> None:
            """Test if create_table() method successfully creates table."""
            await self._repo.create_table()

            async with self.database.enter_connection() as connection:
                result = await connection.run_sync(self._get_table_names)

            self.assertTrue(self._repo.table_name in result)

        async def test_insert_successful(self) -> None:
            """Test if insert method inserts an entry successfully and properly to table."""
            mock_data0 = self._get_mock_data()[0]

            await self._repo.insert(mock_data0)

            rows = await self._get_all_inserted_rows()
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0], mock_data0)

        async def test_insert_successful_many_entries(self) -> None:
            """Test if insert method inserts many entries successfully and properly to table."""
            mock_data = self._get_mock_data()
            to_insert = (mock_data[0], mock_data[2])
            await self._repo.insert(to_insert)

            rows = await self._get_all_inserted_rows()
            self.assertEqual(len(rows), 2)
            self.assertSetEqual(set(rows), set(to_insert))

        async def test_insert_ignore_on_duplicate(self) -> None:
            """Test if insert method inserts entries properly 
            with ignore_on_duplicate argument set to True"""
            mock_data = self._get_mock_data()
            await self._repo.insert(mock_data[0])

            rows = await self._get_all_inserted_rows()
            self.assertEqual(len(rows), 1)
            self.assertSetEqual(
                set(rows),
                set((mock_data[0],))
            )

            # Insert the same data again. This shouldn't insert.
            await self._repo.insert(mock_data[1], ignore_on_duplicate=True)
            self.assertEqual(len(rows), 1)
            self.assertSetEqual(
                set(rows),
                set((mock_data[0],))
            )

        async def test_insert_replace_on_duplicate(self) -> None:
            """Test if insert method replace duplicate entries properly 
            with replace_on_duplicate argument set to True"""
            mock_data = self._get_mock_data()
            await self._repo.insert(mock_data[0])

            # Insert the same data again. This should replace previous insert
            await self._repo.insert(mock_data[3], replace_on_duplicate=True)
            rows = await self._get_all_inserted_rows()
            self.assertEqual(len(rows), 1)
            row = rows[0]
            self.assertEqual(row, mock_data[3])

        async def test_insert_replace_specific_column(self) -> None:
            mock_data = self._get_mock_data()
            modified_column_name = mock_data[-1]
            await self._repo.insert(mock_data[0])

            # Insert the same data again. This should replace previous insert
            await self._repo.insert(mock_data[3], replace_on_duplicate=True, columns_to_replace=[modified_column_name])

            # Assert that only 'columns_to_replace' was changed
            rows = await self._get_all_inserted_rows()
            self.assertEqual(len(rows), 1)
            row = rows[0]
            non_modified_values_lambda = lambda x: {k: v for k, v in x.items() if k != modified_column_name}
            modified_values_lambda = lambda x: {k: v for k, v in x.items() if k == modified_column_name}
            self.assertEqual(non_modified_values_lambda(row), non_modified_values_lambda(mock_data[3]))
            self.assertNotEqual(modified_values_lambda(row), modified_values_lambda(mock_data[0]))

        async def test_delete_successful(self) -> None:
            """Test if delete() method deletes 1 target entry properly."""
            mock_data0 = self._get_mock_data()[0]
            await self._repo.insert(mock_data0)
            id_ = self._get_value_of_primary_key(mock_data0)
            logger.debug(id_)

            await self._repo.delete(id_)

            rows = await self._get_all_inserted_rows()
            logger.debug(rows)
            self.assertEqual(len(rows), 0)

        async def test_is_exists_return_correct_value(self) -> None:
            """Test if is_exist() method correctly finds if value exists."""
            mock_data = self._get_mock_data()

            mock_data0 = mock_data[0]
            await self._repo.insert(mock_data0)
            id_ = self._get_value_of_primary_key(mock_data0)

            is_exists = await self._repo.is_exists(id_)
            self.assertTrue(is_exists)

            id2 = self._get_value_of_primary_key(mock_data[2])
            is_exist2 = await self._repo.is_exists(id2)  # type: ignore
            self.assertFalse(is_exist2)

        # override
        async def asyncTearDown(self) -> None:
            await self._repo.truncate()
            await self.database.engine.dispose()
            return await super().asyncTearDown()

        async def _get_all_inserted_rows(self) -> Sequence[T]:
            async with self.database.enter_session() as session:
                result = await session.execute(select(self._repo.get_model_cls()))
                rows = result.scalars().all()
            return rows

        def _get_value_of_primary_key(self, entity: T) -> ID:
            pk_columns = inspect(self._repo.get_model_cls()).primary_key
            if len(pk_columns) == 1:
                col_ = pk_columns[0]
                value = getattr(entity, col_.name)
                return value
            else:
                values = [getattr(entity, col.name) for col in pk_columns]
                return values  # type: ignore

        @staticmethod
        def _get_table_names(connection: Connection) -> list[str]:
            inspector = inspect(connection)
            return inspector.get_table_names()

        @abstractmethod
        def _get_mock_data(self) -> tuple[T, T, T, T, str]:
            """Create tuple of mock data to be tested by test methods.
            Second mock data is a duplicate of the first.
            Third mock data is duplicate of first with different primary key value.
            Fourth mock data is duplicate of first, with different value on columns with no unique constraints.
            5th element of the tuple is the column name that was modified on fourth mock data.

            Returns
            -------
            tuple[T, ...]
                Mock test data.
            """
            ...

        @property
        @abstractmethod
        def _repo(self) -> Repository[T, ID]:
            """Database repository corresponding to the repository being tested."""
            ...
