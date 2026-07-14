import requests
from app.crud import insert_report
from app.database import create_tables

URL = "https://www.ocso.com/calls-for-service/"

def scrape_ocso():
    print("Scraping OCSO (JSON API)...")
    create_tables()

    response = requests.get(URL)
    data = response.json()

    # The JSON contains a list of active calls
    calls = data.get("data", [])

    for call in calls:
        type_ = call.get("call_type", "Unknown")
        location = call.get("location", "Unknown")
        description = call.get("description", "")
        created_at = call.get("date_time", "")

        insert_report(type_, location, description, created_at)

    print(f"Scrape complete. Inserted {len(calls)} reports.")
