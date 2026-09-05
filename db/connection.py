from db_config import get_db


def execute_query(query, params=None):
    conn = get_db()

    try:
        cur = conn.cursor()
        cur.execute(query, params or ())

        rows = cur.fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()
