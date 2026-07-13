from fastapi import FastAPI
from routers.reports import router as reports_router
from app.database import get_connection

app = FastAPI()

app.include_router(reports_router)

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
