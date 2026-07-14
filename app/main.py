from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
# Routers
from app.routers.reports import router as reports_router
# Database connection (used by stats endpoints)
from app.database import get_connection

app = FastAPI()

# Include your reports router FIRST
app.include_router(reports_router)

# Mount static folder AFTER routers
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Homepage → redirect to reports page
@app.get("/")
def home():
    return RedirectResponse(url="/api/v1/reports/view")

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


