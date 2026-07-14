from fastapi import FastAPI
from app.routers import reports
from app.database import create_tables
from app.scheduler import start_scheduler

app = FastAPI(
    title="O-County Service Report API",
    version="1.0.0"
)

create_tables()
start_scheduler()

app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])

@app.get("/")
def root():
    return {"message": "API is running"}