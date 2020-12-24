import pytest

from crew.crew_member import CrewMember
from deliveries.contract import Contract
from deliveries.delivery import Delivery
from deliveries.scheduler import Scheduler

# @pytest.fixture
# def contract_api_response():
# return {
# "id": 1,
# "item": "Test Item",
# "crew_requirements": {
# "size": 1,
# "conditions": [],
# },
# "destination": "Test Destination",
# }


@pytest.fixture
def contract(cursor):
    _contract = Contract(
        external_contract_id="1", item="Hi", crew_size=2, destination="Hello"
    )
    _contract.save(cursor)

    return _contract


@pytest.fixture
def delivery(cursor, contract):
    d = Delivery(contract_id=contract.id)
    d.save(cursor)

    return d


@pytest.fixture
def crew_members(cursor):
    cms = [CrewMember(name=n) for n in ["Fry", "Leela", "Bender"]]
    for cm in cms:
        cm.save(cursor)

    return cms


def test_scheduler_crew_selection(cursor, crew_members, delivery):
    Scheduler.assign_crew_members(delivery, cursor)

    delivery_crew_members = delivery.crew_members(cursor)
    assert len(delivery_crew_members) == 2
    assert delivery_crew_members[0].name in ["Fry", "Leela", "Bender"]
    assert delivery_crew_members[1].name in ["Fry", "Leela", "Bender"]
    assert delivery_crew_members[0].name != delivery_crew_members[1].name
