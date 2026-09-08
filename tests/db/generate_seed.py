# scripts/generate_seed.py

import os
from datetime import date, datetime

import psycopg2
from psycopg2.extras import RealDictCursor


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "houblon")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

OUTPUT_FILE = "tests/db/seed.sql"
NB_ROWS_PER_TABLE = 3


def sql_value(value):
    """Convertit une valeur Python en valeur SQL."""

    if value is None:
        return "NULL"

    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"

    if isinstance(value, (datetime, date)):
        return f"'{value.isoformat()}'"

    if isinstance(value, str):
        return "'" + value.replace("'", "''") + "'"

    return str(value)


def get_tables(cursor):
    cursor.execute(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_type = 'BASE TABLE'
        ORDER BY table_name
        """
    )

    return [row["table_name"] for row in cursor.fetchall()]


def main():

    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        cursor_factory=RealDictCursor,
    )

    cur = conn.cursor()

    tables = get_tables(cur)

    os.makedirs("tests/db", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as seed:

        seed.write("-- Fichier généré automatiquement\n\n")

        # TRUNCATE dans l'ordre inverse
        for table in reversed(tables):
            seed.write(
                f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;\n"
            )

        seed.write("\n")

        for table in tables:

            cur.execute(
                f"""
                SELECT *
                FROM {table}
                LIMIT {NB_ROWS_PER_TABLE}
                """
            )

            rows = cur.fetchall()

            if not rows:
                print(f"[INFO] Table {table} vide")
                continue

            print(f"[INFO] {table}: {len(rows)} lignes")

            for row in rows:

                columns = ", ".join(row.keys())

                values = ", ".join(
                    sql_value(value)
                    for value in row.values()
                )

                seed.write(
                    f"INSERT INTO {table} "
                    f"({columns}) "
                    f"VALUES ({values});\n"
                )

            seed.write("\n")

    cur.close()
    conn.close()

    print(f"\n✅ Seed généré : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
