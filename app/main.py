from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.routers import reports
from app.database import create_tables
from app.scheduler import start_scheduler

app = FastAPI(
    title="O-County Service Report API",
    version="1.0.0"
)

# Static files served at /static instead of /
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Database + scheduler
create_tables()
start_scheduler()

# Reports router
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])

# Homepage → redirect to reports page
@app.get("/")
def root():
    return RedirectResponse(url="/api/v1/reports/view")
