import requests
from app.crud import insert_report
from app.database import create_tables

URL = "https://www.ocso.com/wp-admin/admin-ajax.php?action=get_active_calls"

def scrape_ocso():
    print("Scraping OCSO JSON API...")

    # Create the database + tables if they don't exist
    create_tables()

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.ocso.com/calls-for-service/"
    }

    response = requests.get(URL, headers=headers, timeout=15)
    response.raise_for_status()

    data = response.json()
    calls = data.get("data", [])

    for call in calls:
        type_ = call.get("call_type", "Unknown")
        location = call.get("location", "Unknown")
        description = call.get("description", "")
        created_at = call.get("date_time", "")

        insert_report(type_, location, description, created_at)

    print(f"Scrape complete. Inserted {len(calls)} reports.")
