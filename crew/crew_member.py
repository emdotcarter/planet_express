class CrewMember:
    _DB_TABLE = "crew_member"

    def __init__(self, name, id=None):
        self._name = name
        self._id = id

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    def save(self, cursor):
        if self.id is None:
            cursor.execute(
                f"""
                INSERT INTO {self._DB_TABLE} (name)
                VALUES (?);
                """,
                [self._name],
            )

            self._id = cursor.execute("SELECT last_insert_rowid();").fetchone()[0]
        else:
            cursor.execute(
                f"""
                UPDATE {self._DB_TABLE}
                SET name = ?
                WHERE id = ?;
                """,
                [
                    self._name,
                    self.id,
                ],
            )

    @classmethod
    def all(cls, cursor=None):
        crew_member_rows = cursor.execute(
            f"SELECT name, id FROM {cls._DB_TABLE}"
        ).fetchall()

        return [cls(name=cmr[0], id=cmr[1]) for cmr in crew_member_rows]

    @classmethod
    def find_by_ids(cls, ids, cursor=None):
        crew_member_rows = cursor.execute(
            f"""
            SELECT name, id
            FROM {cls._DB_TABLE}
            WHERE id in ({','.join("?" * len(ids))})
            """,
            ids,
        ).fetchall()

        return [cls(name=cmr[0], id=cmr[1]) for cmr in crew_member_rows]
