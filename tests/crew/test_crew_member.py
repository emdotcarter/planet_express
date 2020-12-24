from datetime import datetime, timezone
import pytest

from crew.crew_member import CrewMember


def select_crew_member_from_db(cursor, crew_member_id):
    return cursor.execute(
        """
        SELECT name, id
        FROM crew_member
        WHERE id = ?;
        """,
        [crew_member_id],
    ).fetchall()


def test_init_crew_member():
    crew_member = CrewMember(
        name="Fry",
        id=1,
    )

    assert crew_member.name == "Fry"
    assert crew_member.id == 1


def test_save_crew_member(cursor):
    crew_member = CrewMember(
        name="Fry",
    )

    crew_member.save(cursor)

    crew_member_rows = select_crew_member_from_db(cursor, crew_member.id)
    assert len(crew_member_rows) == 1

    crew_member_row = crew_member_rows[0]
    assert crew_member_row[0] == "Fry"
    assert crew_member_row[1] == crew_member.id
