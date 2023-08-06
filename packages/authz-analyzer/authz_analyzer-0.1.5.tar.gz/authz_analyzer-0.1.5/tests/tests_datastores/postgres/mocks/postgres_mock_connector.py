from dataclasses import dataclass
from types import TracebackType
from typing import List, Optional, Tuple, Type
from unittest.mock import MagicMock


@dataclass
class PostgresMockCursor:
    roles: List[Tuple[str, bool, Optional[str], bool]]
    role_grants: List[Tuple[str, str, str, str, str, str]]
    all_tables: List[Tuple[str, str, str]]

    def get(self):
        postgres_mock = MagicMock(name="PostgresConnectionMock")
        fetchall = MagicMock(name="PostgresFetchAllMock", side_effect=[self.roles, self.role_grants, self.all_tables])

        postgres_mock.fetchall = fetchall

        return postgres_mock

    def __enter__(self):
        self.cursor = self.get()
        return self.cursor

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ):
        self.cursor.fetchall.assert_called()  # type: ignore
