from crew.crew_member import CrewMember
from deliveries.contract import Contract


class Delivery:
    _DB_TABLE = "delivery"
    _DB_CREW_MEMBER_JOIN_TABLE = "delivery_crew_member"

    def __init__(self, contract_id, crew_member_ids=[], delivered_at=None, id=None):
        self._contract_id = contract_id
        self._crew_member_ids = crew_member_ids
        self._delivered_at = delivered_at
        self._id = id

    @property
    def contract_id(self):
        return self._contract_id

    @property
    def crew_member_ids(self):
        return self._crew_member_ids

    @property
    def delivered_at(self):
        return self._delivered_at

    @property
    def id(self):
        return self._id

    def contract(self, cursor):
        contract_row = cursor.execute(
            """
            SELECT external_contract_id, item, crew_size, destination, id
            FROM contract
            WHERE id = ?;
            """,
            [self.contract_id],
        ).fetchone()

        return Contract(
            external_contract_id=contract_row[0],
            item=contract_row[1],
            crew_size=contract_row[2],
            destination=contract_row[3],
            id=contract_row[4],
        )

    def crew_members(self, cursor):
        return CrewMember.find_by_ids(self.crew_member_ids, cursor)

    def save(self, cursor):
        if self.id is None:
            cursor.execute(
                f"""
                INSERT INTO {self._DB_TABLE} (contract_id, delivered_at)
                VALUES (?, ?);
                """,
                [self.contract_id, self.delivered_at],
            )

            self._id = cursor.execute("SELECT last_insert_rowid();").fetchone()[0]
        else:
            cursor.execute(
                f"""
                UPDATE {self._DB_TABLE}
                SET contract_id = ?, delivered_at = ?
                WHERE id = ?;
                """,
                [self.contract_id, self.delivered_at, self.id],
            )

        self._save_delivery_crew_members(cursor)

    def _save_delivery_crew_members(self, cursor):
        cursor.execute(
            f"""
            DELETE FROM {self._DB_CREW_MEMBER_JOIN_TABLE}
            WHERE delivery_id = ?;
            """,
            [self.id],
        )

        for crew_member_id in self.crew_member_ids:
            cursor.execute(
                f"""
                INSERT INTO {self._DB_CREW_MEMBER_JOIN_TABLE} (delivery_id, crew_member_id)
                VALUES (?, ?);
                """,
                [self.id, crew_member_id],
            )

    def assign_crew(self, crew_members, cursor):
        self._crew_member_ids = [cm.id for cm in crew_members]
        self._save_delivery_crew_members(cursor)
