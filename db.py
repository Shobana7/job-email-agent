import sqlite3
from datetime import datetime

DB_NAME = "jobs.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        role TEXT,
        status TEXT,
        confidence REAL,
        last_updated TEXT
    )
    """)

    conn.commit()
    conn.close()


def upsert_application(company, role, status, confidence):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        SELECT id FROM applications
        WHERE company = ? AND role = ?
    """, (company, role))

    existing = c.fetchone()
    now = datetime.utcnow().isoformat()

    if existing:
        c.execute("""
            UPDATE applications
            SET status = ?, confidence = ?, last_updated = ?
            WHERE id = ?
        """, (status, confidence, now, existing[0]))
    else:
        c.execute("""
            INSERT INTO applications (company, role, status, confidence, last_updated)
            VALUES (?, ?, ?, ?, ?)
        """, (company, role, status, confidence, now))

    conn.commit()
    conn.close()


def show_all():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT * FROM applications")
    rows = c.fetchall()

    print("\n=== APPLICATIONS DB ===")
    for r in rows:
        print(r)

    conn.close()
