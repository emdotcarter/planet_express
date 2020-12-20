import sqlite3


def idempotent_table_create(
    cursor, table_name, column_definitions, foreign_key_definitions=[]
):
    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")

    column_sql = ", ".join([" ".join(cd) for cd in column_definitions])
    foreign_key_sql = (
        ", ".join(
            [
                f"FOREIGN KEY({fk[0]}) REFERENCES {fk[1]}"
                for fk in foreign_key_definitions
            ]
        )
        or None
    )
    table_definition_sql = ", ".join(filter(None, [column_sql, foreign_key_sql]))

    cursor.execute(f"CREATE TABLE {table_name} ({table_definition_sql});")
