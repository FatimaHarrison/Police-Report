import sqlite3
import requests
import xml.etree.ElementTree as ET

DB_NAME = "police.db"
OCSO_API = "https://www.ocso.com/wp-admin/admin-ajax.php?action=get_active_calls"

def get_connection():
    return sqlite3.connect(DB_NAME)

def fetch_calls():
    response = requests.get(OCSO_API)
    response.raise_for_status()
    return response.text

def parse_xml(xml_text):
    root = ET.fromstring(xml_text)
    calls = []

    for call in root.findall("CALL"):
        incident = call.get("INCIDENT")
        entrytime = call.find("ENTRYTIME").text
        desc = call.find("DESC").text
        location = call.find("LOCATION").text
        sector = call.find("SECTOR").text
        zone = call.find("ZONE").text
        rd = call.find("RD").text

        calls.append({
            "incident": incident,
            "entrytime": entrytime,
            "desc": desc,
            "location": location,
            "sector": sector,
            "zone": zone,
            "rd": rd
        })

    return calls

def insert_calls(calls):
    conn = get_connection()
    cur = conn.cursor()

    for c in calls:
        cur.execute("""
            INSERT INTO reports (type, location, description)
            VALUES (?, ?, ?)
        """, (c["desc"], c["location"], c["entrytime"]))

    conn.commit()
    conn.close()

def main():
    xml_text = fetch_calls()
    calls = parse_xml(xml_text)
    insert_calls(calls)
    print(f"Inserted {len(calls)} calls into police.db")

if __name__ == "__main__":
    main()