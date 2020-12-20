import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import datetime
import sqlite3

from config import DB_NAME, TEST_DB_NAME
from db_helper import idempotent_table_create

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
        table_name="crew_member_quality",
        column_definitions=[
            ["id", "INTEGER", "PRIMARY KEY", "NOT NULL"],
            ["description", "TEXT", "NOT NULL"],
            ["crew_member_id", "INTEGER", "NOT NULL"],
        ],
        foreign_key_definitions=[["crew_member_id", "crew_member(id)"]],
    )

    idempotent_table_create(
        cursor,
        table_name="delivery",
        column_definitions=[
            ["id", "INTEGER", "PRIMARY KEY", "NOT NULL"],
            ["contract_id", "INTEGER", "NOT NULL"],
            ["delivered_on", "DATETIME", "NOT NULL"],
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

    db_connection.commit()

    cursor.close()
    db_connection.close()
