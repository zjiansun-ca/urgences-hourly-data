import requests
import hashlib
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

URL = "https://www.msss.gouv.qc.ca/professionnels/statistiques/documents/urgences/Releve_horaire_urgences_7jours_nbpers.csv"

MONTREAL_TZ = ZoneInfo("America/Toronto")

data_dir = Path("data")
hash_dir = Path("hashes")
data_dir.mkdir(exist_ok=True)
hash_dir.mkdir(exist_ok=True)

# Get local time
now_local = datetime.now(MONTREAL_TZ)
timestamp = now_local.strftime("%Y-%m-%d_%H-%M")

# Download
response = requests.get(URL, timeout=30)
response.raise_for_status()
content = response.content

# Hash content
content_hash = hashlib.sha256(content).hexdigest()
hash_file = hash_dir / "latest_hash.txt"

# Check for duplicate
if hash_file.exists():
    previous_hash = hash_file.read_text()
    if content_hash == previous_hash:
        print("No data change detected. Skipping save.")
        exit(0)

# Save new data
filename = data_dir / f"urgences_{timestamp}_ET.csv"
with open(filename, "wb") as f:
    f.write(content)

# Update hash
hash_file.write_text(content_hash)

print(f"Saved new snapshot: {filename}")
