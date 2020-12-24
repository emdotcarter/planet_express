from datetime import datetime, timezone

from deliveries.delivery import Delivery


def select_delivery_from_db(cursor, delivery_id):
    return cursor.execute(
        """
        SELECT contract_id, delivered_at, id
        FROM delivery
        WHERE id = ?;
        """,
        [delivery_id],
    ).fetchall()


def select_delivery_crew_members_from_db(cursor, delivery_id):
    return cursor.execute(
        """
        SELECT crew_member_id
        FROM delivery_crew_member
        WHERE delivery_id = ?;
        """,
        [delivery_id],
    ).fetchall()


def test_init_delivery():
    delivered_at = datetime.now(timezone.utc)
    delivery = Delivery(
        contract_id=1, crew_member_ids=[2, 3], delivered_at=delivered_at, id=4
    )

    assert delivery.contract_id == 1
    assert delivery.crew_member_ids == [2, 3]
    assert delivery.delivered_at == delivered_at
    assert delivery.id == 4


def test_save_delivery(cursor):
    delivered_at = datetime.now(timezone.utc)
    delivery = Delivery(
        contract_id=1, crew_member_ids=[2, 3], delivered_at=delivered_at
    )

    delivery.save(cursor)

    delivery_rows = select_delivery_from_db(cursor, delivery.id)
    assert len(delivery_rows) == 1

    delivery_row = delivery_rows[0]
    assert delivery_row[0] == 1
    assert delivery_row[1] == str(delivered_at)
    assert delivery_row[2] == delivery.id

    delivery_crew_member_rows = select_delivery_crew_members_from_db(
        cursor, delivery.id
    )
    assert len(delivery_crew_member_rows) == 2
