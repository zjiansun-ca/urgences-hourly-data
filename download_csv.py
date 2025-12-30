import requests
import csv
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

API_URL = "https://www.donneesquebec.ca/recherche/api/3/action/datastore_search"
RESOURCE_ID = "b256f87f-40ec-4c79-bdba-a23e9c50e741"

params = {
    "resource_id": RESOURCE_ID,
    "limit": 100000
}

response = requests.get(API_URL, params=params, timeout=60)
response.raise_for_status()

data = response.json()

records = data["result"]["records"]
fields = [f["id"] for f in data["result"]["fields"]]

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

now = datetime.now(ZoneInfo("America/Toronto"))
timestamp = now.strftime("%Y-%m-%d_%H-%M")

outfile = data_dir / f"urgence_{timestamp}.csv"

with open(outfile, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(records)

print(f"Saved {outfile}")
