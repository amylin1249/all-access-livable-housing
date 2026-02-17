import csv
from typing import NamedTuple
from pathlib import Path

from datetime import datetime

## Clean 311 data


class Encampment(NamedTuple):
    caseid: int
    year: int
    month: int
    date_time: datetime
    latitude: float
    longitude: float
    neighborhood: str
    status_notes: str


DATA_DIR = Path(__file__).parent / "data"


### data - reformat into new csv that generalizes dates into year and month and preserve lat/lon
def clean_311():

    file_input = DATA_DIR / "311_cases.csv"

    with open(file_input, newline="") as csvfile:
        """
        Given a CSV containing 311, return a list of Encampment objects.
        """
        output = []
        reader = csv.DictReader(csvfile)
        for row in reader:
            ### Clean the date ####
            datetime_str = row.get("Opened").replace(" PM", "")
            datetime_str = datetime_str.replace(" AM", "")
            datetime_object = datetime.strptime(datetime_str, "%m/%d/%Y %H:%M:%S")
            date_year = datetime_object.year
            date_month = datetime_object.month

            tuple_out = Encampment(
                row.get("CaseID"),
                date_year,
                date_month,
                datetime_object,
                float(row.get("Latitude")),
                float(row.get("Longitude")),
                row.get("Neighborhood"),
                row.get("Status Notes").lower(),
            )
            output.append(tuple_out)

    return output
