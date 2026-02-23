import httpx
import csv
import os


def get_eviction_data():
    """

    return list of named tuples (lat, lon, YYYY-MM)
    """
    url = "https://data.sfgov.org/resource/5cei-gny5.json"
    params = {"$limit": 50000}

    resp = httpx.get(url, params=params)
    datas = resp.json()

    eviction_list = []

    for data in datas:
        location = data.get("client_location")
        date_raw = data.get("file_date")

        if location and date_raw:
            #  check if in the data
            lat = location.get("latitude")
            lon = location.get("longitude")

            if lat and lon:
                # save as tuple
                record = (float(lat), float(lon), date_raw[:7])
                eviction_list.append(record)

    return eviction_list


def save_eviction_to_csv(data_list, filename="clean-data/evictions_api_data.csv"):
    """
    save api_eviction as a csv file
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["lat", "lon", "year_month"])
        writer.writerows(data_list)


if __name__ == "__main__":
    result = get_eviction_data()
    if result:
        save_eviction_to_csv(result)
