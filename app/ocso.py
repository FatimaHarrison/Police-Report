import requests
from bs4 import BeautifulSoup
from app.database import get_connection


def report_exists(incident_type, location, description, created_at):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id
        FROM reports
        WHERE type = ?
          AND location = ?
          AND description = ?
          AND created_at = ?
    """, (incident_type, location, description, created_at))

    exists = cur.fetchone() is not None
    conn.close()

    return exists


def insert_report(incident_type, location, description, created_at):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reports (type, location, description, created_at)
        VALUES (?, ?, ?, ?)
    """, (
        incident_type,
        location,
        description,
        created_at
    ))

    conn.commit()
    conn.close()


def scrape_ocso():
    url = "https://www.ocso.com/wp-admin/admin-ajax.php?action=get_active_calls"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error downloading active calls: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    calls = soup.find_all("call")

    inserted = 0
    skipped = 0

    for call in calls:
        entry = call.find("entrytime")
        desc = call.find("desc")
        loc = call.find("location")

        if not entry or not desc or not loc:
            continue

        created_at = entry.text.strip()
        incident_type = desc.text.strip()
        location = loc.text.strip()
        description = incident_type

        if report_exists(
            incident_type,
            location,
            description,
            created_at
        ):
            skipped += 1
            continue

        insert_report(
            incident_type,
            location,
            description,
            created_at
        )
        inserted += 1

    print(f"Inserted: {inserted}")
    print(f"Skipped duplicates: {skipped}")


if __name__ == "__main__":
    scrape_ocso()