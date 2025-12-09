import json
import datetime
from pathlib import Path
import requests

# Create /data directory
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

def extract_weather_data(lat=17.3850, lon=78.4867, days=1):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,windspeed_10m",
        "forecast_days": days,
        "timezone": "auto"
    }

    # Make API request
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()

    # Save file with timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = DATA_DIR / f"weather_data_{timestamp}.json"
    filename.write_text(json.dumps(data, indent=2))

    print(f"Weather data extracted to {filename}")
    return data


if __name__ == "__main__":
    extract_weather_data()
