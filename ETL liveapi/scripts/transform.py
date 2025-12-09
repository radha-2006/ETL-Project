import pandas as pd
import os
import json
import glob

def transform_weather_data():
    os.makedirs("../data/staged", exist_ok=True)
    latest_file=sorted1 = sorted(glob.glob("../data/weather_data_*.json"))[-1]
    with open(latest_file, 'r') as f:
        data = json.load(f)

    hourly_data = data['hourly']
    df = pd.DataFrame({"time": hourly_data['time'],
                      "temperature_2m": hourly_data['temperature_2m'],
                      "humidity_percent": hourly_data['relative_humidity_2m'],
                      "wind_speed_kmh": hourly_data['windspeed_10m']})
    df["city"] = "Hyderabad"
    df["extracted_at"] = pd.Timestamp.now()

    output_path="../data/staged/weather_cleaned.csv"
    df.to_csv(output_path, index=False)
    print(f"Transformed {len(df)} weather records saved to {output_path}")
    return df
if __name__ == "__main__":
    transform_weather_data()