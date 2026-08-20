from datetime import datetime
import psycopg
from .config import DATABASE_URL


def get_connection():
    return psycopg.connect(DATABASE_URL)


def add_url_to_db(name):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO urls (name, created_at) 
                VALUES (%s, %s) RETURNING id""",
                (name, datetime.now())
            )
            url_id = cur.fetchone()[0]
        conn.commit()
    return url_id


def url_exists(name):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id FROM urls WHERE name = %s",
                (name,)
            )
            existing_url = cur.fetchone()
    return existing_url is not None



def select_urls():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM urls ORDER BY created_at DESC")
            return cur.fetchall()

def select_url_by_id(url_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, created_at FROM urls WHERE id = %s",
                (url_id,)
            )
            return cur.fetchone()