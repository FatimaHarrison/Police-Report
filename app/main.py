from fastapi import FastAPI
from app.routers import reports
from app.database import create_tables
from app.scheduler import start_scheduler
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(
    title="O-County Service Report API",
    version="1.0.0"
)

# ⭐ Mount your frontend folder here
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# ⭐ Route to serve your dashboard
@app.get("/dashboard")
def dashboard():
    return FileResponse("frontend/index.html")

create_tables()
start_scheduler()

app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])

@app.get("/")
def root():
    return {"message": "API is running"}
