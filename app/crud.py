from app.database import get_connection

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

    cur.execute("SELECT COUNT(*) FROM reports")
    total = cur.fetchone()[0]

    conn.close()
    return total

def get_report_by_id(report_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM reports WHERE id = ?", (report_id,))
    row = cur.fetchone()

    conn.close()
    return row

def create_report(report):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reports (type, location, description, created_at)
        VALUES (?, ?, ?, ?)
    """, (report.type, report.location, report.description, report.created_at))

    conn.commit()
    conn.close()

    return {
        "id": cur.lastrowid,
        "type": report.type,
        "location": report.location,
        "description": report.description,
        "created_at": report.created_at
    }
