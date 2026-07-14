from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.routers import reports
from app.database import create_tables, get_connection
from app.scheduler import start_scheduler

app = FastAPI(
    title="O-County Service Report API",
    version="1.0.0"
)

# Initialize DB + Scheduler
create_tables()
start_scheduler()

# Mount static folder
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Homepage → redirect to reports page
@app.get("/")
def home():
    return RedirectResponse(url="/api/v1/reports/view")

# Include main reports router
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])

# -----------------------------
# 📊 Charts / Stats Endpoints
# -----------------------------

# Incident counts for bar chart
@app.get("/api/v1/reports/stats/incident-counts")
def incident_counts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT type, COUNT(*) AS count
        FROM reports
        GROUP BY type
        ORDER BY count DESC
    """)

    rows = cur.fetchall()
    conn.close()

    return [{"type": r["type"], "count": r["count"]} for r in rows]

# Timeline for line chart
@app.get("/api/v1/reports/stats/timeline")
def timeline():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT created_at, COUNT(*) AS count
        FROM reports
        GROUP BY created_at
        ORDER BY created_at ASC
    """)

    rows = cur.fetchall()
    conn.close()

    return [{"time": r["created_at"], "count": r["count"]} for r in rows]
