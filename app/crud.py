import sqlite3
from app.schemas import ReportCreate, Report

# -------------------------
# Database Helper
# -------------------------

def get_connection():
    return sqlite3.connect("police.db")

# -------------------------
# CRUD Operations
# -------------------------

def create_report(report: ReportCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO reports (type, location, description)
        VALUES (?, ?, ?)
        """,
        (report.type, report.location, report.description)
    )

    conn.commit()
    conn.close()
    return {"status": "created"}

def get_all_reports():
    conn = get_connection()
    cur = conn.cursor()

    rows = cur.execute(
        "SELECT id, type, location, description, created_at FROM reports"
    ).fetchall()

    conn.close()

    return [
        {
            "id": row[0],
            "type": row[1],
            "location": row[2],
            "description": row[3],
            "created_at": row[4]
        }
        for row in rows
    ]

def get_report_by_id(report_id: int):
    conn = get_connection()
    cur = conn.cursor()

    row = cur.execute(
        "SELECT id, type, location, description, created_at FROM reports WHERE id = ?",
        (report_id,)
    ).fetchone()

    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "type": row[1],
        "location": row[2],
        "description": row[3],
        "created_at": row[4]
    }

def update_report(report_id: int, report: ReportCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE reports
        SET type = ?, location = ?, description = ?
        WHERE id = ?
        """,
        (report.type, report.location, report.description, report_id)
    )

    conn.commit()
    updated = cur.rowcount
    conn.close()

    return updated > 0

def delete_report(report_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM reports WHERE id = ?", (report_id,))
    conn.commit()

    deleted = cur.rowcount
    conn.close()

    return deleted > 0
