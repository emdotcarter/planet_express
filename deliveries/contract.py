class Contract:
    _DB_TABLE = "contract"

    def __init__(
        self,
        external_contract_id,
        item,
        crew_size,
        destination,
        id=None,
    ):
        self._external_contract_id = external_contract_id
        self._item = item
        self._crew_size = crew_size
        self._destination = destination
        self._id = id

    @property
    def external_contract_id(self):
        return self._external_contract_id

    @property
    def item(self):
        return self._item

    @property
    def crew_size(self):
        return self._crew_size

    @property
    def destination(self):
        return self._destination

    @property
    def id(self):
        return self._id

    def save(self, cursor):
        if self._id is None:
            cursor.execute(
                f"""
                INSERT INTO {self._DB_TABLE} (external_contract_id, item, crew_size, destination)
                VALUES (?, ?, ?, ?);
                """,
                [
                    self.external_contract_id,
                    self.item,
                    self.crew_size,
                    self.destination,
                ],
            )

            self._id = cursor.execute("SELECT last_insert_rowid();").fetchone()[0]
        else:
            cursor.execute(
                f"""
                UPDATE {self._DB_TABLE}
                SET external_contract_id = ?, item = ?, crew_size = ?, destination = ?
                WHERE id = ?;
                """,
                [
                    self.external_contract_id,
                    self.item,
                    self.crew_size,
                    self.destination,
                    self.id,
                ],
            )
