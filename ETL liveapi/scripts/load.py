import os
import time
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL or KEY missing. Check your .env file!")

SUPABASE = create_client(SUPABASE_URL, SUPABASE_KEY)

def load_to_supabase():
    # Correct file name in your VS Code
    csv_path = "../data/staged/weather_cleaned.csv"

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"{csv_path} not found. Run transform.py first.")

    df = pd.read_csv(csv_path)

    df["time"] = pd.to_datetime(df["time"]).dt.strftime('%Y-%m-%d %H:%M:%S')
    df["extracted_at"] = pd.to_datetime(df["extracted_at"]).dt.strftime('%Y-%m-%d %H:%M:%S')

    batch_size = 20

    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size].fillna("NULL").to_dict("records")

        values = [
            f"('{r['time']}', {r.get('temperature_c','NULL')}, "
            f"{r.get('humidity_percent','NULL')}, {r.get('wind_speed_kmph','NULL')}, "
            f"'{r.get('city','Hyderabad')}', '{r['extracted_at']}')"
            for r in batch
        ]

        insert_sql = f"""
        INSERT INTO weather_data 
        (time, temperature_c, humidity_percent, wind_speed_kmph, city, extracted_at)
        VALUES {', '.join(values)};
        """

        SUPABASE.rpc("execute_sql", {"sql": insert_sql}).execute()

        print(f"Inserted batch {i//batch_size + 1} with {len(batch)} records.")
        time.sleep(0.5)

    print("Data loading completed successfully.")

if __name__ == "__main__":
    load_to_supabase()
