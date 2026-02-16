import csv
from pathlib import Path
from shapely.geometry import Point, Polygon
from typing import NamedTuple


POPULATION_PATH = "data/census/acs_sf_population_2020_24.csv"
RENT_PATH = "data/census/acs_sf_median_rent_2020_24.csv"
HH_INCOME_PATH = "data/census/acs_sf_median_hh_income_2020_24.csv"
RACE_PATH = "data/census/acs_sf_race_2020_24.csv"

POPULATION_ID = "AUO6E001"
RENT_ID = "AUWGE001"
HH_INCOME_ID = "AURUE001"
WHITE_POP_ID = "AUO7E002"


class CleanedData(NamedTuple):
    id: str
    data: int


def clean_acs_data(file_path: str, col_name: str) -> list[CleanedData]:
    """
    This function will load the data from the ACS files saved and 
    return a list of CleanedData tuples.
    
    In each file:
    - Tracts will be identified by their GeoID ("TL_GEO_ID")
    - Data to be saved will be found in the column with the unique identifier

    Parameters:
        col_name: Identifier for the column with the relevant data in that file  
    
    Returns:
        A list of CleanedData items.
    """
    cleaned_data = []
    
    with open(Path(__file__).parent / file_path) as f:
        reader = csv.DictReader(f)

        for row in reader:
            geoid = row["TL_GEO_ID"]
            data = row[col_name]
            if data >= 0:
                cleaned_data.append(CleanedData(geoid, data))

    return cleaned_data


def join_census_tracts(): 
    """
    Docstring for join_census_tracts
    """
    pass