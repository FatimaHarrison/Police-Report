from fastapi import APIRouter, HTTPException, Query
from typing import List
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

from app.schemas import ReportCreate
from app import crud
from app.database import get_connection

router = APIRouter()

# -----------------------------
# Pydantic Response Model
# -----------------------------
class Report(BaseModel):
    id: int
    type: str
    location: str
    description: str
    created_at: str


# -----------------------------
# HTML VIEW WITH PAGINATION
# -----------------------------
@router.get("/view", response_class=HTMLResponse)
def view_reports(limit: int = 10, offset: int = 0):
    reports = crud.get_all_reports(limit=limit, offset=offset)
    total = crud.count_reports()
    current_page = offset // limit + 1
    total_pages = (total + limit - 1) // limit

    html = """
    <html>
    <head>
        <title>O-County Police Reports</title>
        <style>
            body { font-family: Times New Roman; padding: 20px; background: #27B0F5; margin: 0;}
            .report { background: #A9C3D1; padding: 15px; margin-bottom: 15px; border-radius: 8px; }
            .type { font-size: 20px; font-weight: bold; color: #37B320; margin-bottom: 10px;}
            .time { font-size: 15px; color: #134008; margin-top: 10px;}
            .meta { color: #080B40; margin-top: 5px; font-family: Times New Roman;}
            .container { max-width: 900px; margin: center; }
            h1 { text-align: center; margin-bottom: 30px; color: #333; }
            .pagination { text-align: center; margin-top: 30px; }
            .pagination a {
                display: inline-block;
                padding: 8px 14px;
                margin: 3px;
                border: 1px solid #ccc;
                background: #0F282E;
                color: #333;
                text-decoration: none;
                border-radius: 4px;
                font-size: 14px;
            }
            .pagination a:hover { background: #6D8991; }
            .pagination .current { background: #6B51B8; color: white; border-color: #007bff; }
            .pagination .disabled {
                background: #e0e0e0;
                color: #888;
                border-color: #d0d0d0;
                pointer-events: none;
            }
        </style>
    </head>
    <body>
        <h1>O-County Service Reports</h1>
    """

    for r in reports:
        html += f"""
        <div class="report">
            <div class="type">{r['type']}</div>
            <div class="meta">Location: {r['location']}</div>
            <div class="meta">Description: {r['description']}</div>
            <div class="meta">Time: {r['created_at']}</div>
        </div>
        """

    # Pagination
    html += '<div class="pagination">'

    first_offset = 0
    html += f'<a href="/api/v1/reports/view?limit={limit}&offset={first_offset}">Beginning</a>'

    prev_offset = max(0, offset - limit)
    html += f'<a href="/api/v1/reports/view?limit={limit}&offset={prev_offset}">Back</a>'

    for page in range(1, total_pages + 1):
        page_offset = (page - 1) * limit
        class_name = "current" if page == current_page else ""
        html += f'<a class="{class_name}" href="/api/v1/reports/view?limit={limit}&offset={page_offset}">{page}</a>'

    next_offset = offset + limit
    if next_offset >= total:
        html += f'<a class="disabled">Next</a>'
    else:
        html += f'<a href="/api/v1/reports/view?limit={limit}&offset={next_offset}">Forward</a>'

    last_offset = (total_pages - 1) * limit
    html += f'<a href="/api/v1/reports/view?limit={limit}&offset={last_offset}">Last</a>'

    html += "</div></body></html>"

    return html


# -----------------------------
# CRUD ENDPOINTS
# -----------------------------
@router.post("/", response_model=Report)
def create_report(report: ReportCreate):
    created = crud.create_report(report)
    return created


@router.get("/", response_model=List[Report])
def get_reports(limit: int = 10, offset: int = 0):
    return crud.get_all_reports(limit=limit, offset=offset)


@router.get("/{report_id}", response_model=Report)
def get_report(report_id: int):
    report = crud.get_report_by_id(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.put("/{report_id}", response_model=Report)
def update_report_endpoint(report_id: int, report: ReportCreate):
    updated = crud.update_report(report_id, report)
    if updated is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return updated


@router.delete("/{report_id}")
def delete_report_endpoint(report_id: int):
    deleted = crud.delete_report(report_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"status": "deleted"}


# -----------------------------
# NEW: DATE FILTER ENDPOINT
# -----------------------------
@router.get("/filter/date", response_model=List[Report])
def filter_by_date(date: str = Query(..., description="Format: YYYY-MM-DD")):
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


# -----------------------------
# NEW: BAR CHART DATA (incident counts)
# -----------------------------
@router.get("/stats/incident-counts")
def incident_counts(date: str):
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


# -----------------------------
# NEW: LINE CHART DATA (timeline)
# -----------------------------
@router.get("/stats/timeline")
def timeline(date: str):
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
