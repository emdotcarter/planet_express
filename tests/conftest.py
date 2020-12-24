import sqlite3
import pytest

from config import TEST_DB_NAME


@pytest.fixture
def cursor():
    connection = sqlite3.connect(TEST_DB_NAME)
    connection.isolation_level = None

    _cursor = connection.cursor()
    try:
        _cursor.execute("BEGIN")
        yield _cursor
    finally:
        _cursor.execute("ROLLBACK")
        connection.close()
