import pytest
import sqlite3

from config import TEST_DB_NAME


@pytest.fixture
def cursor():
    connection = sqlite3.connect(TEST_DB_NAME)
    connection.isolation_level = None

    cursor = connection.cursor()
    try:
        cursor.execute("BEGIN")
        yield cursor
    finally:
        cursor.execute("ROLLBACK")
        connection.close()
