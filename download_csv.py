from pathlib import Path
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

URL = (
    "https://www.donneesquebec.ca/recherche/dataset/"
    "fichier-horaire-des-donnees-de-la-situation-a-l-urgence/"
    "resource/b256f87f-40ec-4c79-bdba-a23e9c50e741/"
    "download/fichier-horaire-donnees-situation-urgence.csv"
)

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

now = datetime.now(ZoneInfo("America/Toronto"))
timestamp = now.strftime("%Y-%m-%d_%H-%M")

response = requests.get(URL, timeout=60)
response.raise_for_status()

outfile = data_dir / f"urgence_{timestamp}.csv"
outfile.write_bytes(response.content)

print(f"Saved {outfile}")
