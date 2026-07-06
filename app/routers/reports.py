from fastapi import APIRouter, HTTPException
from app.schemas import ReportCreate
from app import crud

router = APIRouter()

# -------------------------
# Create a new report
# -------------------------
@router.post("/")
def create_report(report: ReportCreate):
    return crud.create_report(report)

# -------------------------
# Get all reports
# -------------------------
@router.get("/")
def get_reports():
    return crud.get_all_reports()

# -------------------------
# Get a report by ID
# -------------------------
@router.get("/{report_id}")
def get_report(report_id: int):
    report = crud.get_report_by_id(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@router.put("/{report_id}")
def update_report_endpoint(report_id: int, report: ReportCreate):
    updated = crud.update_report(report_id, report)
    if not updated:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"status": "updated"}

@router.delete("/{report_id}")
def delete_report_endpoint(report_id: int):
    deleted = crud.delete_report(report_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"status": "deleted"}
