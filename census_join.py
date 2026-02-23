import csv
import sys
import pandas as pd
import geopandas as gpd


SF_CENSUS_PATH = "raw-data/census/sf_census_tracts_2020.csv"
CALI_TRACTS_SHP = "raw-data/census/cali_tracts_shapefiles/tl_2025_06_tract.shp"

POP_PATH = "raw-data/census/acs_sf_population_2020_24.csv"
RENT_PATH = "raw-data/census/acs_sf_median_rent_2020_24.csv"
HH_INC_PATH = "raw-data/census/acs_sf_median_hh_income_2020_24.csv"
RACE_PATH = "raw-data/census/acs_sf_race_2020_24.csv"

SF_ACS_JOIN = "clean-data/census_acs_join.csv"
SF_TRACTS_SHP = "clean-data/sf_shapefiles/sf_tracts.shp"
MERGED_SF_TRACTS_SHP = "clean-data/merged_sf_shapefiles/merged_sf_tracts.shp"

POP_ID = "AUO6E001"
RENT_ID = "AUWGE001"
HH_INC_ID = "AURUE001"
WHITE_POP_ID = "AUO7E002"

KEYS = ["geo_id", "population", "med_rent", "med_hh_inc", "white_pct"]


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


def join_acs_data():
    """
    Docstring
    """
    ### Change function to use PD?
    csv.field_size_limit(sys.maxsize)

    cleaned_pop_acs = clean_acs_data(POP_PATH, POP_ID)
    cleaned_race_acs = clean_acs_data(RACE_PATH, WHITE_POP_ID)
    cleaned_rent_acs = clean_acs_data(RENT_PATH, RENT_ID)
    cleaned_hh_inc_acs = clean_acs_data(HH_INC_PATH, HH_INC_ID)

    with open(SF_CENSUS_PATH) as f:
        reader = csv.DictReader(f)

        with open(SF_ACS_JOIN, "w") as f:
            writer = csv.DictWriter(f, KEYS)
            writer.writeheader()

            for row in reader:
                geo_id = row["geoid"]
                population = cleaned_pop_acs[geo_id]

                if population > 0:
                    white_pct = cleaned_race_acs[geo_id] / population
                else:
                    white_pct = None

                writer.writerow(
                    {
                        KEYS[0]: geo_id,
                        KEYS[1]: population,
                        KEYS[2]: cleaned_rent_acs[geo_id],
                        KEYS[3]: cleaned_hh_inc_acs[geo_id],
                        KEYS[4]: white_pct,
                    }
                )


def get_sf_geoid() -> list[str]:
    """
    Extract the list of SF census tract GeoIDs based on the list of 2020 census
    tracts from DataSF Open Data Portal

    Returns:
        List of SF census tract GeoIDs
    """
    sf_geoid = []

    csv.field_size_limit(sys.maxsize)

    with open(SF_CENSUS_PATH) as f:
        reader = csv.DictReader(f)
        for row in reader:
            sf_geoid.append(row["geoid"])

    return sf_geoid


def create_sf_shapefiles():
    """
    Filter California census tract shapefiles and create SF census tract
    shapefiles that only include tracts in San Francisco, by matching with the
    GeoIDs obtained from the San Francisco list of census tracts.
    """
    cali_tracts = gpd.read_file(CALI_TRACTS_SHP)
    sf_geoid = get_sf_geoid()
    sf_tracts = cali_tracts[cali_tracts["GEOID"].isin(sf_geoid)]

    sf_tracts.to_file(SF_TRACTS_SHP)


def add_sf_tract_data():
    """
    Add SF ACS data to SF census tract shapefiles as attributes
    """
    sf_tracts = gpd.read_file(SF_TRACTS_SHP)
    sf_acs_data = pd.read_csv(SF_ACS_JOIN, dtype={"geo_id": "str"})

    # Align geo_id column name in sf_acs_data with GEOID column name in
    # sf_tracts shapefile
    sf_acs_data.rename(columns={"geo_id": "GEOID"}, inplace=True)

    updated_sf_tracts = sf_tracts.merge(sf_acs_data, on="GEOID", how="left")
    updated_sf_tracts.to_file(MERGED_SF_TRACTS_SHP)

    return sf_acs_data


if __name__ == "__main__":
    join_acs_data()
    create_sf_shapefiles()
    add_sf_tract_data()
