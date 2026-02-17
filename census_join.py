import csv
import sys
from pathlib import Path
from shapely.geometry import Point, Polygon
from typing import NamedTuple


SF_CENSUS_PATH = "data/census/sf_census_tracts_2020.csv"
POP_PATH = "data/census/acs_sf_population_2020_24.csv"
RENT_PATH = "data/census/acs_sf_median_rent_2020_24.csv"
HH_INC_PATH = "data/census/acs_sf_median_hh_income_2020_24.csv"
RACE_PATH = "data/census/acs_sf_race_2020_24.csv"

POP_ID = "AUO6E001"
RENT_ID = "AUWGE001"
HH_INC_ID = "AURUE001"
WHITE_POP_ID = "AUO7E002"

KEYS = ["geo_id", "geom", "population", "median_rent", "median_hh_income", "white_pct"]


# class CleanedData(NamedTuple):
#     id: str
#     data: int


def clean_acs_data(file_path: str, col_name: str) -> dict:
    """
    This function will load the data from the ACS files saved and
    return a list of CleanedData tuples.

    In each file:
    - Tracts will be identified by their GeoID ("TL_GEO_ID")
    - Data to be saved will be found in the column with the unique identifier

    Parameters:
        col_name: Identifier for the column with the relevant data in that file

    Returns:
        A dictionary of GeoID keys that map to their data fields
        (None if the original data is a negative value)
    """
    cleaned_data = {}

    with open(file_path) as f:
        reader = csv.DictReader(f)

        for row in reader:
            geo_id = row["TL_GEO_ID"]
            data = int(row[col_name])
            if data >= 0:
                cleaned_data[geo_id] = data
            else:
                cleaned_data[geo_id] = None

    return cleaned_data


def join_census_tracts():
    """
    Docstring for join_census_tracts
    """
    csv.field_size_limit(sys.maxsize)

    with open(SF_CENSUS_PATH) as f:
        reader = csv.DictReader(f)

        with open("census_acs_join.csv", "w") as f:
            writer = csv.DictWriter(f, KEYS)
            writer.writeheader()

            for row in reader:
                geom = row["the_geom"]
                geo_id = row["geoid"]
                population = clean_acs_data(POP_PATH, POP_ID)[geo_id]

                if population > 0:
                    white_pct = (
                        clean_acs_data(RACE_PATH, WHITE_POP_ID)[geo_id] / population
                    )
                else:
                    white_pct = None

                if geom.startswith("MULTIPOLYGON") and geo_id:
                    writer.writerow(
                        {
                            KEYS[0]: geo_id,
                            KEYS[1]: geom,
                            KEYS[2]: population,
                            KEYS[3]: clean_acs_data(RENT_PATH, RENT_ID)[geo_id],
                            KEYS[4]: clean_acs_data(HH_INC_PATH, HH_INC_ID)[geo_id],
                            KEYS[5]: white_pct,
                        }
                    )


if __name__ == "__main__":
    join_census_tracts()
