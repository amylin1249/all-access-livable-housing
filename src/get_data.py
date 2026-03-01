import httpx
import csv
import os
import time
from pathlib import Path
from datetime import datetime


def get_evictions_data() -> list[tuple]:
    """
    Provides coordinates and dates of evictions in San Francisco

    Returns:
        List of tuples (id, lat, lon, YYYY-MM)
    """
    url = "https://data.sfgov.org/resource/5cei-gny5.json"
    params = {"$limit": 50000}

    resp = httpx.get(url, params=params)
    datas = resp.json()

    eviction_list = []
    current_id = 1
    for data in datas:
        location = data.get("client_location")
        date_raw = data.get("file_date")

        if location and date_raw:
            #  check if in the data
            lat = location.get("latitude")
            lon = location.get("longitude")

            if lat and lon:
                # save as tuple
                date_obj = datetime.strptime(date_raw, "%Y-%m-%dT%H:%M:%S.%f")
                date = date_obj.strftime("%Y-%m")
                record = (int(current_id),float(lat), float(lon), date)
                eviction_list.append(record)
                current_id += 1

    return eviction_list


def save_evictions_to_csv(data_list, filename="clean-data/evictions_api_data.csv"):
    """
    Save data from evictions API as a csv file
    """
    os.makedirs(os.path.dirname(Path(__file__).parent.parent / filename), exist_ok=True)

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id","lat", "lon", "year_month"])
        writer.writerows(data_list)


def get_shelter_data():
    """
    [Currently not in use -- keeping it here for the time being]
    Get monthly counts of people on the shelter waitlist, and the number of days
    to which we have data access.

    Returns:
        counts_per_month: Total counts of people on the shelter waitlist for a
                          given month
        days_per_month: Total number of days to which we have data access for a
                        given month
    """
    REQUEST_DELAY = 1
    EXPORT_URL_TEMPLATE = "https://data.sfgov.org/api/archival.csv?id=w4sk-nq57&version=VERSION&method=export"
    API_URL = (
        "https://data.sfgov.org/api/publishing/v1/revision/w4sk-nq57/changes?cursor="
    )

    export_url = EXPORT_URL_TEMPLATE
    next_page_url = API_URL

    # Total counts of people on waitlist in any given month
    counts_per_month = {}

    # Number of days that had data for any given month
    days_per_month = {}

    # Dummy value to ensure shelters_next_page is not 0 and will run in while loop
    shelters_next_page = 1

    while shelters_next_page:
        # Access first page of hidden API (i.e., most recent records)
        time.sleep(REQUEST_DELAY)
        shelters_json = httpx.get(next_page_url).json()

        # Get key fields of each record (i.e., counts per day)
        for record in shelters_json["resource"]:
            version = record["value"]["version"]
            year_month = record["value"]["created_at"][:7]
            export_url = EXPORT_URL_TEMPLATE.replace("VERSION", str(version))

            time.sleep(REQUEST_DELAY)
            export_resp = httpx.get(export_url)

            # Only include URLs that autodownload CSV file in the counts;
            # excludes any URL that leads to timeout error
            if export_resp.headers.get("Content-Type").startswith("text/csv"):
                # Split data into rows, excluding header and last blank row
                data = export_resp.text.split("\n")[1:-1]

                counts_per_month[year_month] = counts_per_month.get(
                    year_month, 0
                ) + len(data)
                days_per_month[year_month] = days_per_month.get(year_month, 0) + 1

        shelters_next_page = shelters_json["meta"]["next"]
        if shelters_next_page:
            next_page_url = API_URL + shelters_next_page

    return counts_per_month, days_per_month


if __name__ == "__main__":
    result = get_evictions_data()
    if result:
        save_evictions_to_csv(result)
