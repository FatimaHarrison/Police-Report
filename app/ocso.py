import sqlite3
import requests
from bs4 import BeautifulSoup

DB_NAME = "police.db"
OCSO_API = "https://www.ocso.com/wp-admin/admin-ajax.php?action=get_active_calls"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_calls():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(OCSO_API, headers=headers)
    response.raise_for_status()
    return response.text

def parse_html(raw):
    soup = BeautifulSoup(raw, "html.parser")
    rows = soup.find_all("tr")

    calls = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue

        entrytime = cols[0].text.strip()
        incident = cols[1].text.strip()
        location = cols[2].text.strip()
        desc = cols[3].text.strip()

        calls.append({
            "incident": incident,
            "entrytime": entrytime,
            "desc": desc,
            "location": location
        })

    return calls

def call_exists(conn, incident, location, entrytime):
    cur = conn.cursor()
    cur.execute("""
        SELECT id FROM reports
        WHERE type = ? AND location = ? AND description = ?
    """, (incident, location, entrytime))
    return cur.fetchone() is not None

def insert_calls(calls):
    conn = get_connection()
    cur = conn.cursor()

    inserted = 0
    skipped = 0

    for c in calls:
        if call_exists(conn, c["incident"], c["location"], c["entrytime"]):
            skipped += 1
            continue

        cur.execute("""
            INSERT INTO reports (type, location, description)
            VALUES (?, ?, ?)
        """, (c["incident"], c["location"], c["entrytime"]))

        inserted += 1

    conn.commit()
    conn.close()

    print(f"Inserted: {inserted}, Skipped duplicates: {skipped}")

def main():
    raw = fetch_calls()
    calls = parse_html(raw)
    insert_calls(calls)

if __name__ == "__main__":
    main()
