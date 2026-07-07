from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel

from app.schemas import ReportCreate
from app import crud

router = APIRouter()

# -------------------------
# Pydantic Response Model
# -------------------------
class Report(BaseModel):
    id: int
    type: str
    location: str
    description: str
    created_at: str


# -------------------------
# Create a new report
# -------------------------
@router.post("/", response_model=Report)
def create_report(report: ReportCreate):
    created = crud.create_report(report)
    return created


# -------------------------
# Get all reports
# -------------------------
@router.get("/", response_model=List[Report])
def get_reports():
    return crud.get_all_reports()


# -------------------------
# Get a report by ID
# -------------------------
@router.get("/{report_id}", response_model=Report)
def get_report(report_id: int):
    report = crud.get_report_by_id(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


# -------------------------
# Update a report
# -------------------------
@router.put("/{report_id}", response_model=Report)
def update_report_endpoint(report_id: int, report: ReportCreate):
    updated = crud.update_report(report_id, report)
    if updated is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return updated


# -------------------------
# Delete a report
# -------------------------
@router.delete("/{report_id}")
def delete_report_endpoint(report_id: int):
    deleted = crud.delete_report(report_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"status": "deleted"}
