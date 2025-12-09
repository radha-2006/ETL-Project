import json
import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
STAGED_DIR = Path(__file__).resolve().parent.parent / "data" / "staged"
STAGED_DIR.mkdir(parents=True, exist_ok=True)

def transform_apod(raw_file):
    with open(raw_file, "r") as f:
        data = json.load(f)

    df = pd.DataFrame([{
        "date": data.get("date"),
        "title": data.get("title"),
        "explanation": data.get("explanation"),
        "media_type": data.get("media_type"),
        "url": data.get("url"),
        "hdurl": data.get("hdurl")
    }])

    output_path = STAGED_DIR / f"apod_cleaned_{data['date']}.csv"
    df.to_csv(output_path, index=False)

    print(f"🔄 Transformed → {output_path}")
    return output_path

if __name__ == "__main__":
    latest_raw = sorted(RAW_DIR.glob("*.json"))[-1]
    transform_apod(latest_raw)
