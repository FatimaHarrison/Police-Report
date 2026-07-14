import sqlite3

DB_PATH = "police.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            location TEXT,
            description TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()
