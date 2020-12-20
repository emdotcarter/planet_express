class Delivery:
    _DB_TABLE_NAME = "delivery"

    def __init__(
        self, id, contract_id, crew_members=[], delivered_on=None, cursor=None
    ):
        self._id = id
        self._contract_id = contract_id
        self._crew_members = crew_members
        self._delivered_on = delivered_on
        self._cursor = cursor

    def _db_cursor(self):
        return self._cursor or sqlite3.connect(DB_NAME).cursor()

    def save(self):
        self._db_cursor().execute(
            f"INSERT INTO {self._DB_TABLE_NAME} (contract_id) VALUES (?);",
            [self._contract_id],
        )

    def assign_crew_member(self, crew_member):
        pass
