#Declaring imports from the SQLIte database using the app schemes as queries,
#to import a creating report. 
import sqlite3
from app.schemas import ReportCreate
from app.database import get_db as get_connection


# Method to use for to help the database. 
def get_connection():
    conn = sqlite3.connect("police.db")
    conn.row_factory = sqlite3.Row  # allows dict-like row access
    return conn

# CRUD Operations to modify data from the database and JSON file. 
def create_report(report: ReportCreate):
    conn = get_connection()
    cur = conn.cursor()
 #Method to insert data into the reports table. 
    cur.execute(
        """
        INSERT INTO reports (type, location, description, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (report.type, report.location, report.description, report.created_at)
    )

    conn.commit()
    new_id = cur.lastrowid
    conn.close()
  # Return clean matching Pydantic model, clean JSON display. 
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

    rows = cur.execute(
        """
        SELECT id, type, location, description, created_at
        FROM reports
        ORDER BY id DESC
        LIMIT ? OFFSET ?
        """,
        (limit, offset)
    ).fetchall()

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

    row = cur.execute(
        "SELECT id, type, location, description, created_at FROM reports WHERE id = ?",
        (report_id,)
    ).fetchone()

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

    cur.execute(
        """
        UPDATE reports
        SET type = ?, location = ?, description = ?, created_at = ?
        WHERE id = ?
        """,
        (report.type, report.location, report.description, report.created_at, report_id)
    )

    conn.commit()
    updated = cur.rowcount
    conn.close()

    if updated == 0:
        return None

    # Return updated report as clean dict
    return {
        "id": report_id,
        "type": report.type,
        "location": report.location,
        "description": report.description,
        "created_at": report.created_at
    }

#Deleting reports
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

    total = cur.execute("SELECT COUNT(*) FROM reports").fetchone()[0]

    conn.close()
    return total

# -----------------------------------------
# CRUD: Get reports by a specific date
# -----------------------------------------
def get_reports_by_date(date: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, type, location, description, created_at
        FROM reports
        WHERE DATE(created_at) = DATE(?)
        ORDER BY created_at DESC
    """, (date,))

    rows = cur.fetchall()
    conn.close()

    return [dict(r) for r in rows]

# CRUD: Incident counts for bar chart
def get_incident_counts(date: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT type, COUNT(*) AS count
        FROM reports
        WHERE DATE(created_at) = DATE(?)
        GROUP BY type
        ORDER BY count DESC
    """, (date,))

    rows = cur.fetchall()
    conn.close()

    return [dict(r) for r in rows]

# CRUD: Timeline counts for line chart

def get_timeline_counts(date: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT strftime('%H:%M', created_at) AS time, COUNT(*) AS count
        FROM reports
        WHERE DATE(created_at) = DATE(?)
        GROUP BY time
        ORDER BY time ASC
    """, (date,))

    rows = cur.fetchall()
    conn.close()

    return [dict(r) for r in rows]