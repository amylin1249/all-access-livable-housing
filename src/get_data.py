import httpx
import csv
import os
import time
from pathlib import Path
from datetime import datetime

REQUEST_DELAY = 0.1

def get_evictions_data() -> list[tuple]:
    """
    Provides coordinates and dates of evictions in San Francisco

    Returns:
        List of tuples (id, lat, lon, YYYY-MM)
    """
    url = "https://data.sfgov.org/resource/5cei-gny5.json"
    
    time.sleep(REQUEST_DELAY)
    params = {"$limit": 50000}

    resp = httpx.get(url, params=params)
    datas = resp.json()

    eviction_list = []
    current_id = 1
    for data in datas:
        location = data.get("client_location")
        date_raw = data.get("file_date")

        if location and date_raw:

            date_obj = datetime.strptime(date_raw, "%Y-%m-%dT%H:%M:%S.%f")
            year = date_obj.year

            #filter years(2020-2024)
            if 2020<= year <=2024:

            #  check if in the data
                lat = location.get("latitude")
                lon = location.get("longitude")

                if lat and lon:
                # save as tuple
                    date = date_obj.strftime("%Y-%m")
                    record = {
                        "id" : int(current_id),
                        "lat": float(lat), 
                        "lon":float(lon), 
                        "year_mon" : date
                    }
                eviction_list.append(record)
                current_id += 1

    return eviction_list


def save_evictions_to_csv(data_list, filename="clean-data/evictions_api_data.csv"):
    """
    Save data from evictions API as a csv file
    """
    os.makedirs(os.path.dirname(Path(__file__).parent.parent / filename), exist_ok=True)
    fieldnames = ["id", "lat", "lon", "year_mon"]
    with open(filename, "w", newline="") as f:
        csv_writer = csv.DictWriter(f, fieldnames = fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(data_list)


if __name__ == "__main__":
    result = get_evictions_data()
    if result:
        save_evictions_to_csv(result)
