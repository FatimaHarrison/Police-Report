# scraper.py (original working version)
from app.ocso import scrape_ocso
from app.database import create_tables

def main():
    create_tables()
    scrape_ocso()

if __name__ == "__main__":
    main()
