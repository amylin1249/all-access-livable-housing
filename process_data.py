import csv
import sys
import pandas as pd
import numpy as np
import geopandas as gpd
from typing import NamedTuple
from pathlib import Path
from openpyxl import load_workbook
from datetime import datetime
import jellyfish

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

EXCLUDE_GEOIDS = ["06075980401", "06075980200"]


class encampment(NamedTuple):
    tents: int
    structures: int
    vehicles: int

    year: int
    month: int
    date_time: datetime
    latitude: float
    longitude: float
    neighborhood: str
   

class encampment_report(NamedTuple):
    caseid: int
    year: int
    month: int
    date_time: datetime
    latitude: float
    longitude: float
    neighborhood: str
    status_notes: str
    report_ids: str

def rate(score):
    if score >= 0.95:
        return "high"
    if score < 0.95 and score >= 0.80:
        return "medium"
    return "low"   


DATA_DIR = Path(__file__).parent / "raw-data"

## Clean 311 data
def clean_311():

    file_input = DATA_DIR / "311_cases.csv"

    with open(file_input, newline="") as csvfile:
        """
        Given a CSV containing 311, return a list of Encampment report objects.
        """
        output_report = []
        reader = csv.DictReader(csvfile)
        for row in reader:
            ### Clean the date ####
            datetime_str = row.get("Opened").replace(" PM", "")
            datetime_str = datetime_str.replace(" AM", "")
            datetime_object = datetime.strptime(datetime_str, "%m/%d/%Y %H:%M:%S")
            date_year = datetime_object.year
            date_month = datetime_object.month

            tuple_out = encampment_report(
                row.get("CaseID"),
                date_year,
                date_month,
                datetime_object,
                float(row.get("Latitude")),
                float(row.get("Longitude")),
                row.get("Neighborhood"),
                row.get("Status Notes").lower(),
                []
            )
            output_report.append(tuple_out)

    return output_report

### Clean encampment data ###
def clean_encampment():
    file_input = DATA_DIR / "Historical Tent Counts.xlsx"
    wb = load_workbook(file_input)
    sheet_obj = wb.active

    for i in range(1, sheet_obj.max_column + 1):
        print(sheet_obj.cell(row=1, column=i).value)

    for i in range(1, sheet_obj.max_column + 1):
        print(sheet_obj.cell(row=2, column=i).value)

    assert sheet_obj.cell(row=2, column=3).value == "Tents"
    assert sheet_obj.cell(row=2, column=4).value == "Structures"
    assert sheet_obj.cell(row=2, column=5).value == "Passenger Vehicles"
    assert sheet_obj.cell(row=2, column=6).value == 'Other Vehicles'
    assert sheet_obj.cell(row=2, column=8).value == 'Neighborhood'
    assert sheet_obj.cell(row=2, column=10).value == 'Latitude'
    assert sheet_obj.cell(row=2, column=11).value == 'Longitude'

    output_encampment = []
    for i in range(3, sheet_obj.max_row+1):

        sheet_obj.cell(row=3, column=1).value 
        date_obj = sheet_obj.cell(row=i, column=1).value
        date_string = date_obj.strftime("%m/%d/%Y")
        tents = sheet_obj.cell(row=i, column=3).value
        structure = sheet_obj.cell(row=i, column=4).value
        vehicles = sheet_obj.cell(row=i, column=5).value + sheet_obj.cell(row=i, column=6).value
        neighborhood = sheet_obj.cell(row=i, column=8).value

        lat = float(sheet_obj.cell(row=i, column=10).value)
        lon = float(sheet_obj.cell(row=i, column=11).value)
        obj = encampment(tents,
        structure,
        vehicles,
        date_obj.year,
        date_obj.month,
        date_string,
        lat,
        lon,
        neighborhood)
        output_encampment.append(obj)
    return output_encampment


#### Merge the two files to filter out 311 reports associatd with marked/observed encampments ####

def attached_311_reports(output_encampment, output_report):

    associated_encamp = []

    for encampment in output_encampment:
        for report in output_report: 
            if report.month == encampment.month and report.year == encampment.year:
                if rate(jellyfish.jaro_winkler_similarity(encampment.neighborhood.lower(), report.neighborhood.lower())) == "high":
                    associated_encamp.append((encampment, report))


def process_acs_data():
    """
    Load the data from the ACS files saved, impute negative or zero values in
    rent and household income, merge them based on GeoID, and save the merged
    dataframe to a new file.

    In each ACS file:
    - Tracts will be identified by their GeoID ("TL_GEO_ID")
    - Data to be merged will be found in the column with the unique identifier
    """
    csv.field_size_limit(sys.maxsize)

    pop_df = pd.read_csv(POP_PATH, usecols=["TL_GEO_ID", POP_ID], dtype={"TL_GEO_ID": "str"})
    race_df = pd.read_csv(RACE_PATH, usecols=["TL_GEO_ID", WHITE_POP_ID], dtype={"TL_GEO_ID": "str"})
    rent_df = pd.read_csv(RENT_PATH, usecols=["TL_GEO_ID", RENT_ID], dtype={"TL_GEO_ID": "str"})
    hh_inc_df = pd.read_csv(HH_INC_PATH, usecols=["TL_GEO_ID", HH_INC_ID], dtype={"TL_GEO_ID": "str"})

    # Impute negative or zero values in rent and household income dataframes
    # with the mean of their positive values
    mean_rent = round(rent_df.loc[rent_df[RENT_ID] > 0, RENT_ID].mean())
    rent_df.loc[rent_df[RENT_ID] <= 0, RENT_ID] = mean_rent

    mean_hh_inc = round(hh_inc_df.loc[hh_inc_df[HH_INC_ID] > 0, HH_INC_ID].mean())
    hh_inc_df.loc[hh_inc_df[HH_INC_ID] <= 0, HH_INC_ID] = mean_hh_inc

    # Rename population, race, rent, and household income column names
    pop_df = pop_df.rename(columns={POP_ID: "population"})
    race_df = race_df.rename(columns={WHITE_POP_ID: "white_pop"})
    rent_df = rent_df.rename(columns={RENT_ID: "med_rent"})
    hh_inc_df = hh_inc_df.rename(columns={HH_INC_ID: "med_hh_inc"})

    # Merge individual dataframes based on GEO_ID 
    joined_df = pd.merge(pop_df, race_df, on="TL_GEO_ID", how='left')
    joined_df = pd.merge(joined_df, rent_df, on="TL_GEO_ID", how='left')
    joined_df = pd.merge(joined_df, hh_inc_df, on="TL_GEO_ID", how='left')

    # Add white_pct to df
    joined_df["white_pct"] = np.where(joined_df["population"] > 0, joined_df["white_pop"] / joined_df["population"], 0)

    joined_df.to_csv(SF_ACS_JOIN, index=False)


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
            geoid = row["geoid"]
            if geoid not in EXCLUDE_GEOIDS:
                sf_geoid.append(geoid)

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
    sf_acs_data = pd.read_csv(SF_ACS_JOIN, dtype={"TL_GEO_ID": "str"})

    # Align geo_id column name in sf_acs_data with GEOID column name in
    # sf_tracts shapefile
    sf_acs_data.rename(columns={"TL_GEO_ID": "GEOID"}, inplace=True)

    updated_sf_tracts = sf_tracts.merge(sf_acs_data, on="GEOID", how="left")
    updated_sf_tracts.to_file(MERGED_SF_TRACTS_SHP)

    return sf_acs_data


if __name__ == "__main__":
    process_acs_data()
    create_sf_shapefiles()
    add_sf_tract_data()
