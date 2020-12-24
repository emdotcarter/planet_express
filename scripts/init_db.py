import os
import sqlite3
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from config import DB_NAME, TEST_DB_NAME  # noqa: E402
from db_helper import idempotent_table_create  # noqa: E402

for db in [DB_NAME, TEST_DB_NAME]:
    db_connection = sqlite3.connect(db)
    cursor = db_connection.cursor()

    idempotent_table_create(
        cursor,
        table_name="crew_member",
        column_definitions=[
            ["id", "INTEGER", "PRIMARY KEY", "NOT NULL"],
            ["name", "TEXT", "NOT NULL"],
        ],
    )

    idempotent_table_create(
        cursor,
        table_name="delivery",
        column_definitions=[
            ["id", "INTEGER", "PRIMARY KEY", "NOT NULL"],
            ["contract_id", "INTEGER", "NOT NULL"],
            ["delivered_at", "DATETIME"],
        ],
        foreign_key_definitions=[
            ["contract_id", "contract(id)"],
        ],
    )

    idempotent_table_create(
        cursor,
        table_name="delivery_crew_member",
        column_definitions=[
            ["delivery_id", "INTEGER", "NOT NULL"],
            ["crew_member_id", "INTEGER", "NOT NULL"],
        ],
        foreign_key_definitions=[
            ["delivery_id", "delivery(id)"],
            ["crew_member_id", "crew_member(id)"],
        ],
    )

    idempotent_table_create(
        cursor,
        table_name="contract",
        column_definitions=[
            ["id", "INTEGER", "PRIMARY KEY", "NOT NULL"],
            ["external_contract_id", "INTEGER", "NOT NULL"],
            ["item", "TEXT", "NOT NULL"],
            ["crew_size", "INTEGER", "NOT NULL"],
            ["destination", "TEXT", "NOT NULL"],
        ],
    )

    db_connection.commit()

    cursor.close()
    db_connection.close()
