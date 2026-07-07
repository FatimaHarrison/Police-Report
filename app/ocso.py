import sqlite3
import requests
from bs4 import BeautifulSoup
import os
from bs4 import XMLParsedAsHTMLWarning
import warnings

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
DB_PATH = os.path.join(os.path.dirname(__file__), "police.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def report_exists(type, location, description, created_at):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id FROM reports
        WHERE type = ? AND location = ? AND description = ? AND created_at = ?
    """, (type, location, description, created_at))

    exists = cur.fetchone()
    conn.close()
    return exists is not None

def insert_report(type, location, description, created_at):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reports (type, location, description, created_at)
        VALUES (?, ?, ?, ?)
    """, (type, location, description, created_at))

    conn.commit()
    conn.close()

def scrape_ocso():
    print("Using database:", DB_PATH)

    url = "https://www.ocso.com/wp-admin/admin-ajax.php?action=get_active_calls"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)

    # The OCSO feed returns HTML inside JSON-like structure
    raw = response.text.strip()

    # Sometimes the feed returns "0" (WordPress failure)
    if raw == "0":
        print("OCSO returned empty response (0).")
        return

    # Extract HTML table rows
    soup = BeautifulSoup(raw, "html.parser")
    rows = soup.find_all("tr")

    inserted = 0
    skipped = 0

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue

        type = cols[1].text.strip()
        location = cols[2].text.strip()
        description = cols[3].text.strip()
        created_at = cols[0].text.strip()

        if report_exists(type, location, description, created_at):
            skipped += 1
            continue

        insert_report(type, location, description, created_at)
        inserted += 1

    print(f"Inserted: {inserted}, Skipped duplicates: {skipped}")

if __name__ == "__main__":
    scrape_ocso()
