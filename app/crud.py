from app.database import get_connection
from app.schemas import ReportCreate


def create_report(report: ReportCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reports (type, location, description, created_at)
        VALUES (?, ?, ?, ?)
    """, (report.type, report.location, report.description, report.created_at))

    conn.commit()
    new_id = cur.lastrowid
    conn.close()

    return {
        "id": new_id,
        "type": report.type,
        "location": report.location,
        "description": report.description,
        "created_at": report.created_at
    }


def get_all_reports(limit: int = 10, offset: int = 0):
    conn = get_connection()
    cur = conn.cursor()

    rows = cur.execute("""
        SELECT id, type, location, description, created_at
        FROM reports
        ORDER BY id DESC
        LIMIT ? OFFSET ?
    """, (limit, offset)).fetchall()

    conn.close()

    return [
        {
            "id": row["id"],
            "type": row["type"],
            "location": row["location"],
            "description": row["description"],
            "created_at": row["created_at"]
        }
        for row in rows
    ]


def get_report_by_id(report_id: int):
    conn = get_connection()
    cur = conn.cursor()

    row = cur.execute("""
        SELECT id, type, location, description, created_at
        FROM reports
        WHERE id = ?
    """, (report_id,)).fetchone()

    conn.close()

    if row is None:
        return None

    return {
        "id": row["id"],
        "type": row["type"],
        "location": row["location"],
        "description": row["description"],
        "created_at": row["created_at"]
    }


def update_report(report_id: int, report: ReportCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE reports
        SET type = ?, location = ?, description = ?, created_at = ?
        WHERE id = ?
    """, (
        report.type,
        report.location,
        report.description,
        report.created_at,
        report_id
    ))

    conn.commit()

    if cur.rowcount == 0:
        conn.close()
        return None

    conn.close()

    return {
        "id": report_id,
        "type": report.type,
        "location": report.location,
        "description": report.description,
        "created_at": report.created_at
    }


def delete_report(report_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM reports WHERE id = ?", (report_id,))
    conn.commit()

    deleted = cur.rowcount > 0

    conn.close()
    return deleted


def count_reports():
    conn = get_connection()
    cur = conn.cursor()

    total = cur.execute(
        "SELECT COUNT(*) FROM reports"
    ).fetchone()[0]

    conn.close()
    return total