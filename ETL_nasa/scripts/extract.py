import os
import requests
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NASA_API_KEY")
BASE_URL = "https://api.nasa.gov/planetary/apod"

# Create raw directory
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

def extract_apod():
    today = datetime.now().strftime("%Y-%m-%d")

    params = {
        "api_key": API_KEY,
        "date": today
    }

    print(f"🔍 Requesting NASA APOD for: {today}")

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return

    data = response.json()

    file_path = RAW_DIR / f"apod_raw_{today}.json"
    file_path.write_text(json.dumps(data, indent=2))

    print(f"📥 Extracted NASA data → {file_path}")
    return file_path

if __name__ == "__main__":
    extract_apod()
