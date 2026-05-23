import os
import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))


def save_email(email: dict, category: str) -> None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO emails (gmail_id, subject, sender, date, snippet, category)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (gmail_id) DO UPDATE
                    SET category = EXCLUDED.category
                """,
                (
                    email["id"],
                    email["subject"],
                    email["from"],
                    email["date"],
                    email["snippet"],
                    category,
                ),
            )
        conn.commit()
    finally:
        conn.close()


def get_emails(category: str | None = None) -> list[dict]:
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if category:
                cur.execute("SELECT * FROM emails WHERE category = %s ORDER BY date DESC", (category,))
            else:
                cur.execute("SELECT * FROM emails ORDER BY date DESC")
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()
