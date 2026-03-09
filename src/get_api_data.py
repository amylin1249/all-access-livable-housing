import httpx
import csv
from pathlib import Path
import time
from datetime import datetime

from .datatypes import CLEAN_EVICTIONS

EVICTIONS_URL = "https://data.sfgov.org/resource/5cei-gny5.json"
REQUEST_DELAY = 1
CLEAN_DATA_DIR = Path(__file__).parent.parent / "clean-data"


def get_evictions_data() -> list[tuple]:
    """
    Retrieve coordinates and dates of evictions in San Francisco from 2020-2024.

    Returns:
        List of tuples (id, lat, lon, YYYY-MM) with coordinates and dates of evictions.
    """
    time.sleep(REQUEST_DELAY)
    params = {"$limit": 50000}

    resp = httpx.get(EVICTIONS_URL, params=params)
    datas = resp.json()

    evictions_list = []
    current_id = 1

    for data in datas:
        location = data.get("client_location")
        date_raw = data.get("file_date")

        if location and date_raw:
            date_obj = datetime.strptime(date_raw, "%Y-%m-%dT%H:%M:%S.%f")
            year = date_obj.year

            # Filter for years of interest (2020-2024)
            if 2020 <= year <= 2024:
                # Check if data has latitude and longitude
                lat = location.get("latitude")
                lon = location.get("longitude")

                if lat and lon:
                    date = date_obj.strftime("%Y-%m")
                    record = {
                        "id": int(current_id),
                        "lat": float(lat),
                        "lon": float(lon),
                        "year_mon": date,
                    }
                    evictions_list.append(record)
                    current_id += 1

    return evictions_list


def save_evictions_to_csv(evictions_list):
    """
    Save data from evictions API as a CSV file
    """
    if not CLEAN_DATA_DIR.exists():
        CLEAN_DATA_DIR.mkdir()
    fieldnames = ["id", "lat", "lon", "year_mon"]
    with open(CLEAN_EVICTIONS, "w", newline="") as f:
        csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(evictions_list)
