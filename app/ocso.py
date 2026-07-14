import sqlite3
import requests
from bs4 import BeautifulSoup
import os

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
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    raw = response.text.strip()

    # Parse XML using html.parser (works on all systems)
    soup = BeautifulSoup(raw, "html.parser")
    calls = soup.find_all("call")  # XML tags become lowercase

    inserted = 0
    skipped = 0

    for call in calls:
        created_at = call.find("entrytime").text.strip()
        type = call.find("desc").text.strip()
        location = call.find("location").text.strip()
        description = type  # same field

        if report_exists(type, location, description, created_at):
            skipped += 1
            continue

        insert_report(type, location, description, created_at)
        inserted += 1

    print(f"Inserted: {inserted}, Skipped duplicates: {skipped}")

if __name__ == "__main__":
    scrape_ocso()
