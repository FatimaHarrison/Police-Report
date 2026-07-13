from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from typing import List
from pydantic import BaseModel
from app import crud
from app.database import get_connection


router = APIRouter()

class Report(BaseModel):
    id: int
    type: str
    location: str
    description: str
    created_at: str

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
            .meta { color: #080B40; margin-top: 5px; font-family: Times New Roman;}
            h1 { text-align: center; margin-bottom: 30px; color: #333; }
            .pagination { text-align: center; margin-top: 30px; }
            .pagination a {
                display: inline-block;
                padding: 8px 14px;
                margin: 3px;
                border: 1px solid #ccc;
                background: #ffc400;
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

    <div style="text-align:center; margin-bottom:20px;">
        <a href="/static/chart.html"
           style="display:inline-block;
                  padding:10px 20px;
                  background:#ffc400;
                  color:#000;
                  text-decoration:none;
                  border-radius:6px;
                  font-weight:bold;
                  font-family:Times New Roman;">
            View Charts
        </a>
    </div>

    <h1>O-County Service Reports</h1>
    """

    # Render each report
    for r in reports:
        html += f"""
        <div class="report">
            <div class="type">{r['type']}</div>
            <div class="meta">Location: {r['location']}</div>
            <div class="meta">Description: {r['description']}</div>
            <div class="meta">Time: {r['created_at']}</div>
        </div>
        """

    # Pagination container
    html += '<div class="pagination">'

    # Beginning button
    html += f'<a href="/api/v1/reports/view?limit={limit}&offset=0">Beginning</a>'

    # Back button
    prev_offset = max(0, offset - limit)
    html += f'<a href="/api/v1/reports/view?limit={limit}&offset={prev_offset}">Back</a>'

    # Limit visible page numbers to 6
    max_pages = 6
    end_page = min(total_pages, max_pages)

    # Page number buttons
    for page in range(1, end_page + 1):
        page_offset = (page - 1) * limit
        class_name = "current" if page == current_page else ""
        html += f'<a class="{class_name}" href="/api/v1/reports/view?limit={limit}&offset={page_offset}">{page}</a>'

    # Forward button
    next_offset = offset + limit
    if next_offset >= total:
        html += f'<a class="disabled">Next</a>'
    else:
        html += f'<a href="/api/v1/reports/view?limit={limit}&offset={next_offset}">Next</a>'

    # Last button
    last_offset = (total_pages - 1) * limit
    html += f'<a href="/api/v1/reports/view?limit={limit}&offset={last_offset}">Last</a>'

    # Close HTML
    html += "</div></body></html>"

    return html
