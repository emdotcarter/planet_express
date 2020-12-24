from datetime import datetime, timezone
import pytest

from deliveries.contract import Contract


def select_contract_from_db(cursor, contract_id):
    return cursor.execute(
        """
        SELECT external_contract_id, item, crew_size, destination, id
        FROM contract
        WHERE id = ?;
        """,
        [contract_id],
    ).fetchall()


def test_init_contract():
    contract = Contract(
        external_contract_id=1,
        item="Hi",
        crew_size=2,
        destination="Hello",
        id=3,
    )

    assert contract.external_contract_id == 1
    assert contract.item == "Hi"
    assert contract.crew_size == 2
    assert contract.destination == "Hello"
    assert contract.id == 3


def test_save_contract(cursor):
    contract = Contract(
        external_contract_id=1,
        item="Hi",
        crew_size=2,
        destination="Hello",
    )

    contract.save(cursor)

    contract_rows = select_contract_from_db(cursor, contract.id)
    assert len(contract_rows) == 1

    contract_row = contract_rows[0]
    assert contract_row[0] == 1
    assert contract_row[1] == "Hi"
    assert contract_row[2] == 2
    assert contract_row[3] == "Hello"
    assert contract_row[4] == contract.id
