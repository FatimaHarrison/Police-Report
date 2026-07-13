import sqlite3
import requests
from bs4 import BeautifulSoup
import os
from app.database import get_connection

URL = "https://www.ocso.com/wp-admin/admin-ajax.php?action=get_active_calls"

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
    print("Scraper running...")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(URL, headers=headers)
    raw = response.text.strip()

    if raw == "0":
        print("OCSO returned empty response (0).")
        return

    soup = BeautifulSoup(raw, "html.parser")
    rows = soup.find_all("tr")

    inserted = 0
    skipped = 0

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue

        created_at = cols[0].text.strip()
        type = cols[1].text.strip()
        location = cols[2].text.strip()
        description = cols[3].text.strip()

        if report_exists(type, location, description, created_at):
            skipped += 1
            continue

        insert_report(type, location, description, created_at)
        inserted += 1

    print(f"Inserted: {inserted}, Skipped: {skipped}")
