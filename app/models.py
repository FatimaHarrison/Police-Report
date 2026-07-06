import sqlite3

# Database Model Setup
def create_tables():
    conn = sqlite3.connect("police.db")
    cur = conn.cursor()

    cur.execute("""
       CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        location TEXT NOT NULL,
        description TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
