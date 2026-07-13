import requests
from bs4 import BeautifulSoup
from app.crud import insert_report
from app.database import create_tables

URL = "https://www.ocso.com/wp-admin/admin-ajax.php?action=get_active_calls"

def scrape_ocso():
    print("Scraping OCSO...")
    create_tables()

    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.select("table tbody tr")

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue

        type_ = cols[0].get_text(strip=True)
        location = cols[1].get_text(strip=True)
        description = cols[2].get_text(strip=True)
        created_at = cols[3].get_text(strip=True)

        insert_report(type_, location, description, created_at)

    print("Scrape complete.")
