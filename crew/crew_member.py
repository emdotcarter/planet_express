from config import DB_NAME
import sqlite3


class CrewMember:
    _DB_TABLE_NAME = "crew_member"

    def __init__(self, id, name, cursor=None):
        self._id = id
        self._name = name
        self._cursor = cursor

    @property
    def name(self):
        return self._name

    def save(self):
        self._db_cursor().execute(
            f"INSERT INTO {self._DB_TABLE_NAME} (name) VALUES (?);", [self._name]
        )

    def _db_cursor(self):
        return self._cursor or sqlite3.connect(DB_NAME).cursor()

    @classmethod
    def available_crew_members(cls):
        crew_member_rows = (
            self._db_cursor()
            .execute(f"SELECT id, name FROM {self._DB_TABLE_NAME}")
            .fetchall()
        )

        return [cls(cmr[0], cmr[1]) for cmr in crew_member_rows]
