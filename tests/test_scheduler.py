import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import sqlite3

from config import TEST_DB_NAME
from crew.crew_member import CrewMember
from deliveries.delivery import Delivery
from deliveries.scheduler import Scheduler


@pytest.fixture
def test_db_cursor():
    connection = sqlite3.connect(TEST_DB_NAME)
    connection.isolation_level = None

    cursor = connection.cursor()
    try:
        cursor.execute("BEGIN")
        yield cursor
    finally:
        cursor.execute("ROLLBACK")
        connection.close()


@pytest.fixture
def contract_api_response():
    return {
        "id": 1,
        "item": "Test Item",
        "crew_requirements": {
            "size": 1,
            "conditions": [],
        },
        "destination": "Test Destination",
    }


@pytest.fixture
def create_delivery():
    def _create_delivery(cursor):
        delivery = Delivery(contract_id=1, cursor=cursor)
        delivery.save()

        return delivery

    return _create_delivery


@pytest.fixture
def create_crew_members():
    def _crew(cursor, names):
        for name in names:
            CrewMember(name, cursor).save()

    return _crew


def test_scheduler_crew_selection(test_db_cursor, create_crew_members, create_delivery):
    create_crew_members(test_db_cursor, ["Fry", "Leela", "Bender"])
    delivery = create_delivery(test_db_cursor)

    Scheduler.assign_crew_members(delivery)

    assert len(delivery.crew_members) == 1
    assert len(delivery.crew_members[0].name) in ["Fry", "Leela", "Bender"]
