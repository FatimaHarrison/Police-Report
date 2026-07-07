from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.schemas import ReportCreate
from app import crud
from fastapi.responses import HTMLResponse
router = APIRouter()

# Pydantic Response Model
class Report(BaseModel):
    id: int
    type: str
    location: str
    description: str
    created_at: str

@router.get("/view", response_class=HTMLResponse)
def view_reports(limit: int = 10, offset: int = 0):
    reports = crud.get_all_reports(limit=limit, offset=offset)

    html = """
    <html>
    <head>
        <title>O-County Police Reports</title>
        <style>
            body { font-family: Times New Roman; padding: 20px; background: #27B0F5; margin: 0;}
            .report { background: #A9C3D1; padding: 15px; margin-bottom: 15px; border-radius: 8px; }
            .type { font-size: 20px; font-weight: bold; color: #37B320; margin-bottom: 10px;}
            .time { font-size: 15px; color: #134008; margin-top: 10px;}
            .meta { color: #555; margin-top: 5px; }
            .container { max-width: 900px; margin: center; }
            h1 { text-align: center; margin-bottom: 30px; color: #333; }
            
        </style>
    </head>
    <body>
        <h1>O-County Service Reports</h1>
    """

    for r in reports:
        html += f"""
        <div class="report">
            <div class="type">{r['type']}</div>S
            <div class="meta">Location: {r['location']}</div>
            <div class="meta">Description: {r['description']}</div>
            <div class="meta">Time: {r['created_at']}</div>
        </div>
        """

    html += "</body></html>"
    return html

# Creating a new report
@router.post("/", response_model=Report)
def create_report(report: ReportCreate):
    created = crud.create_report(report)
    return created

# Get all reports
@router.get("/", response_model=List[Report])
def get_reports(limit: int = 10, offset: int = 0):
    return crud.get_all_reports(limit=limit, offset=offset)


# Get a report by ID
@router.get("/{report_id}", response_model=Report)
def get_report(report_id: int):
    report = crud.get_report_by_id(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

# Update a report
@router.put("/{report_id}", response_model=Report)
def update_report_endpoint(report_id: int, report: ReportCreate):
    updated = crud.update_report(report_id, report)
    if updated is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return updated
# Delete a report
@router.delete("/{report_id}")
def delete_report_endpoint(report_id: int):
    deleted = crud.delete_report(report_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"status": "deleted"}
