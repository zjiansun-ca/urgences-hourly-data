import requests
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo  # Built-in in Python 3.9+

URL = "https://www.msss.gouv.qc.ca/professionnels/statistiques/documents/urgences/Releve_horaire_urgences_7jours_nbpers.csv"

# Montreal / Eastern Time
MONTREAL_TZ = ZoneInfo("America/Toronto")

output_dir = Path("data")
output_dir.mkdir(exist_ok=True)

# Local Montreal time with DST handled automatically
now_local = datetime.now(MONTREAL_TZ)
timestamp = now_local.strftime("%Y-%m-%d_%H-%M")

filename = output_dir / f"urgences_{timestamp}_ET.csv"

response = requests.get(URL, timeout=30)
response.raise_for_status()

with open(filename, "wb") as f:
    f.write(response.content)

print(f"Saved {filename}")
