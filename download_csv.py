import requests
import hashlib
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

URL = "https://www.msss.gouv.qc.ca/professionnels/statistiques/documents/urgences/Releve_horaire_urgences_7jours_nbpers.csv"

MONTREAL_TZ = ZoneInfo("America/Toronto")

data_dir = Path("data")
hash_dir = Path("hashes")
data_dir.mkdir(exist_ok=True)
hash_dir.mkdir(exist_ok=True)

now_local = datetime.now(MONTREAL_TZ)
timestamp = now_local.strftime("%Y-%m-%d_%H-%M")

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; DataCollectionBot/1.0)"
}

MAX_RETRIES = 5
WAIT_SECONDS = 15

content = None

for attempt in range(1, MAX_RETRIES + 1):
    try:
        print(f"Attempt {attempt} downloading data...")
        response = requests.get(URL, headers=headers, timeout=30)
        response.raise_for_status()
        content = response.content
        break
    except requests.exceptions.RequestException as e:
        print(f"Attempt {attempt} failed: {e}")
        if attempt < MAX_RETRIES:
            time.sleep(WAIT_SECONDS)
        else:
            print("All attempts failed. Exiting gracefully.")
            exit(0)  # Do NOT crash the workflow

# Hash content
content_hash = hashlib.sha256(content).hexdigest()
hash_file = hash_dir / "latest_hash.txt"

if hash_file.exists() and hash_file.read_text() == content_hash:
    print("No data change detected.")
    exit(0)

filename = data_dir / f"urgences_{timestamp}_ET.csv"
with open(filename, "wb") as f:
    f.write(content)

hash_file.write_text(content_hash)

print(f"Saved new snapshot: {filename}")
