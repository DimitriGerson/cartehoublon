import os

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

#BASE_DIR = Path(__file__).resolve().parent
#DB = BASE_DIR / "Houblon.db"

def get_db():
    conn = psycopg.connect(
        host="localhost",
        port=5432,
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        row_factory=dict_row
    )
    return conn
