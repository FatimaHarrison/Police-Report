import requests
from bs4 import BeautifulSoup
from app.crud import insert_report
from app.database import create_tables

URL = "https://www.ocso.com/calls-for-service/"

def scrape_ocso():
    print("Scraping OCSO (HTML table)...")
    create_tables()

    response = requests.get(URL, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")
    if not table:
        print("ERROR: Could not find call table.")
        return

    rows = table.find_all("tr")[1:]  # skip header

    count = 0
    for row in rows:
        cols = [c.get_text(strip=True) for c in row.find_all("td")]
        if len(cols) != 4:
            continue

        call_number, date_time, call_type, location = cols

        insert_report(
            call_type,
            location,
            f"Call #{call_number}",
            date_time
        )

        count += 1

    print(f"Scrape complete. Inserted {count} reports.")
