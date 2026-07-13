from app.database import get_connection

def insert_report(type, location, description, created_at):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reports (type, location, description, created_at)
        VALUES (?, ?, ?, ?)
    """, (type, location, description, created_at))

    conn.commit()
    conn.close()

def get_all_reports(limit=10, offset=0):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM reports
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
    """, (limit, offset))

    rows = cur.fetchall()
    conn.close()
    return rows

def count_reports():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) AS total FROM reports")
    total = cur.fetchone()["total"]

    conn.close()
    return total
