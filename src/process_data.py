import csv
import sys
import pandas as pd
import numpy as np
import geopandas as gpd
import jellyfish
from typing import NamedTuple
from pathlib import Path
from openpyxl import load_workbook
from datetime import datetime
from datatypes import (
    SF_CENSUS_PATH,
    CALI_TRACTS_SHP,
    POP_PATH,
    RENT_PATH,
    HH_INC_PATH,
    RACE_PATH,
    RENTER_UNITS_PATH,
    REPORT_PATH,
    ENCAMP_PATH,
    SF_ACS_JOIN,
    SF_TRACTS_SHP,
    MERGED_SF_TRACTS_SHP,
    POP_ID,
    RENT_ID,
    HH_INC_ID,
    WHITE_POP_ID,
    RENTER_UNITS_ID,
)


REPORT_PATH = (
    Path(__file__).parent.parent / "raw-data"/ "311_cases.csv"
)
ENCAMP_PATH = (
      Path(__file__).parent.parent / "raw-data"/ "encampment_counts.xlsx"
)

HH_INC_PATH = (
    Path(__file__).parent.parent / "raw-data/census/acs_sf_median_hh_income_2020_24.csv"
)
RACE_PATH = Path(__file__).parent.parent / "raw-data/census/acs_sf_race_2020_24.csv"
RENTER_UNITS_PATH = Path(__file__).parent.parent / "raw-data/census/acs_sf_housing_units_2020_24.csv"

SF_ACS_JOIN = Path(__file__).parent.parent / "clean-data/census_acs_join.csv"
SF_TRACTS_SHP = Path(__file__).parent.parent / "clean-data/sf_shapefiles/sf_tracts.shp"
MERGED_SF_TRACTS_SHP = (
    Path(__file__).parent.parent
    / "clean-data/merged_sf_shapefiles/merged_sf_tracts.shp"
)

POP_ID = "AUO6E001"
RENT_ID = "AUWGE001"
HH_INC_ID = "AURUE001"
WHITE_POP_ID = "AUO7E002"
RENTER_UNITS_ID = "AUUEE003"

EXCLUDE_GEOIDS = ["06075980401", "06075980200"]

class Encampment(NamedTuple):
    ### unique  encampmemnt id per quarter
    id: int
    tents: int
    structures: int
    vehicles: int

    year: int
    month: int
    date_time: datetime
    lat: float
    lon: float
    neighborhood: str


class EncampmentReport(NamedTuple):
    id: int
    year: int
    month: int
    address: str
    lat: float
    lon: float
  


def rate(score):
    if score >= 0.95:
        return "high"
    if score < 0.95 and score >= 0.80:
        return "medium"
    return "low"

### LILY CLEANING PROCESS ###

STOPWORDS = [
    "st",
    "street",
    "av",
    "avenue",
    "ave",
    "av",
    "blvd",
    "boulevard",
    "rd",
    "road",
    "ln",
    "lane",
    "dr",
    "drive",
    "ct",
    "court",
    "pkwy",
    "parkway",
    "dr",
    "drive",
    "ter",
    "terrace",
    "cir",
    "circle",
    "pl",
    "place",
    "stwy",
    "a",
    "an",
    "and",
    "&",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "he",
    "in",
    "is",
    "it",
    "its",
    "of",
    "on",
    "that",
    "the",
    "to",
    "was",
    "were",
    "will",
    "with",
    "park",
    "parks",
    "intersection",
]


PUNCTUATION = ".,?-#/()[]"


def clean_parenthesis(phrase):
    """
    This function takes a phrase and removes any parenthesized portion.

    Parameters:
        * phrase: a string representing a phrase

    Returns:
        A string representing the phrase with parenthesized portion removed.
    """
    phrase = phrase.replace("(", "*(")
    phrase = phrase.replace(")", ")*")

    split_phrase = phrase.split("*")
    output_list = []

    for word in split_phrase:
        if word == "":
            continue
        elif word[0] != "(" and word[-1] != ")":
            output_list.append(word.strip())

    return " ".join(output_list)


def clean_address(address):
    address = address.lower()
    address = address.replace("i poi", "")
    address = clean_parenthesis(address)
    text_data = address.split(" ")
    cleaned_list = [word.strip(PUNCTUATION) for word in text_data]
    cleaned_list = [word for word in cleaned_list if word != ""]
    cleaned_list = [word for word in cleaned_list if word not in STOPWORDS]
    return " ".join(cleaned_list)

### AMY INGESTION AND APPLICATION OF CLEANING PROCESS ###

def generate_311_csv():
    # Load raw data
    df = pd.read_csv("raw-data/311_cases.csv")

    # Keep only necessary columns
    df = df[["Opened", "Address", "Latitude", "Longitude"]]

    # Rename columns for ease of spatial join
    df = df.rename(
        columns={
            "Opened": "date",
            "Address": "address",
            "Latitude": "lat",
            "Longitude": "lon",
        }
    )

    # Convert date to standardized format: YYYY-MM
    df["date"] = pd.to_datetime(df["date"])
    df["date"] = df["date"].dt.strftime("%Y-%m")

    # Filter for years of interest: 2020-2024
    df = df[df["date"].between("2020-01-01", "2024-12-31")]

    # Add id column
    df["id"] = range(1, len(df) + 1)

    # Clean addresses
    df["address"] = df["address"].apply(clean_address)

    # De-dupe by cleaned address and month (keep only one row per cleaned
    # address per month)
    df = df.drop_duplicates(subset=["address", "date"], keep="first")

    # Drop address as it's no longer needed after this point
    df = df.drop(columns=["address"])

    # Reorder columns for readability
    df = df.reindex(columns=["id", "date", "lat", "lon"])

    df.to_csv("clean-data/clean_311_data.csv", index=False)

### Clean encampments ###
def generate_encampments_csv():
    # Top row (row 0) is not a real header row
    df = pd.read_excel("raw-data/encampment_counts.xlsx", header=1)

    # Keep only necessary columns
    df = df[
        [
            "Observed",
            "Tents",
            "Structures",
            "Passenger Vehicles",
            "Other Vehicles",
            "Latitude",
            "Longitude",
        ]
    ]

    # Rename columns for ease of spatial join
    df = df.rename(
        columns={
            "Observed": "date",
            "Tents": "tents",
            "Structures": "structures",
            "Latitude": "lat",
            "Longitude": "lon",
        }
    )

    # Convert date to standardized format: YYYY-MM
    df["date"] = pd.to_datetime(df["date"])
    df["date"] = df["date"].dt.strftime("%Y-%m")

    # Filter for years of interest: 2020-2024
    df = df[df["date"].between("2020-01-01", "2024-12-31")]

    # Aggregate passenger and other vehicles
    df["vehicles"] = df["Passenger Vehicles"].astype(int) + df["Other Vehicles"].astype(
        int
    )

    # Remove unused passenger and other vehicles columns
    df = df.drop(columns=["Passenger Vehicles", "Other Vehicles"])

    # Add id column
    df["id"] = range(1, len(df) + 1)

    # Reorder to keep vehicles next to tents and structures
    df = df.reindex(
        columns=["id", "date", "tents", "structures", "vehicles", "lat", "lon"]
    )

    df.to_csv("clean-data/clean_encampments_data.csv", index=False)



### Bounding box
### neighborhood bound
# ### For each encampment, create a bounding box for each encampmemnt
### use the timeit library
### timeit helpful to see which functions are taking the longest


def process_acs_data():
    """
    Load the data from the ACS files saved, impute negative or zero values in
    rent and household income, merge them based on GeoID, and save the merged
    dataframe to a new file.

    In each ACS file:
    - Tracts will be identified by their GeoID ("TL_GEO_ID")
    - Data to be merged will be found in the column with the unique identifier
    """
    # Read in ACS CSV files as dataframes and specify columns of interest
    pop_df = pd.read_csv(
        POP_PATH, usecols=["TL_GEO_ID", POP_ID], dtype={"TL_GEO_ID": "str"}
    )
    race_df = pd.read_csv(
        RACE_PATH, usecols=["TL_GEO_ID", WHITE_POP_ID], dtype={"TL_GEO_ID": "str"}
    )
    rent_df = pd.read_csv(
        RENT_PATH, usecols=["TL_GEO_ID", RENT_ID], dtype={"TL_GEO_ID": "str"}
    )
    hh_inc_df = pd.read_csv(
        HH_INC_PATH, usecols=["TL_GEO_ID", HH_INC_ID], dtype={"TL_GEO_ID": "str"}
    )
    renter_df = pd.read_csv(
        RENTER_UNITS_PATH,
        usecols=["TL_GEO_ID", RENTER_UNITS_ID],
        dtype={"TL_GEO_ID": "str"},
    )

    # Impute negative or zero values (i.e., missing) in rent and household income
    # dataframes with the mean of their positive values
    mean_rent = round(rent_df.loc[rent_df[RENT_ID] > 0, RENT_ID].mean())
    rent_df.loc[rent_df[RENT_ID] <= 0, RENT_ID] = mean_rent

    mean_hh_inc = round(hh_inc_df.loc[hh_inc_df[HH_INC_ID] > 0, HH_INC_ID].mean())
    hh_inc_df.loc[hh_inc_df[HH_INC_ID] <= 0, HH_INC_ID] = mean_hh_inc

    # Merge individual dataframes based on GEO_ID
    joined_df = pop_df
    for df in [race_df, rent_df, hh_inc_df, renter_df]:
        joined_df = pd.merge(joined_df, df, on="TL_GEO_ID", how="left")

    # Rename population, race, rent, income, and renter units column names
    joined_df = joined_df.rename(columns={POP_ID: "population",
                                          WHITE_POP_ID: "white_pop",
                                          RENT_ID: "med_rent",
                                          HH_INC_ID: "med_hh_inc",
                                          RENTER_UNITS_ID: "rent_units"})

    # Add calculation of percentage of white population per tract as a new column
    joined_df["white_pct"] = np.where(
        joined_df["population"] > 0, joined_df["white_pop"] / joined_df["population"], 0
    )

    joined_df.to_csv(SF_ACS_JOIN, index=False)


def get_sf_geoid() -> list[str]:
    """
    Extract the list of SF census tract GeoIDs based on the list of 2020 census
    tracts from DataSF Open Data Portal.

    Returns:
        List of SF census tract GeoIDs
    """
    sf_geoid = []

    csv.field_size_limit(sys.maxsize)

    with open(SF_CENSUS_PATH) as f:
        reader = csv.DictReader(f)
        for row in reader:
            geoid = row["geoid"]
            if geoid != EXCLUDE_GEOID:
                sf_geoid.append(geoid)

    return sf_geoid


def create_sf_shapefiles():
    """
    Filter California census tract shapefiles and create SF census tract
    shapefiles that only include tracts in San Francisco, by matching with the
    GeoIDs obtained from the San Francisco list of census tracts.
    """
    cali_tracts = gpd.read_file(CALI_TRACTS_SHP)

    # Filter California tract IDs only for those that are in SF
    sf_tracts = cali_tracts[cali_tracts["GEOID"].isin(get_sf_geoid())]

    sf_tracts.to_file(SF_TRACTS_SHP)


def add_sf_tract_data():
    """
    Add SF ACS data to SF census tract shapefiles as attributes, and save to new
    SF census tract shapefiles containing the merged attributes.
    """
    sf_tracts = gpd.read_file(SF_TRACTS_SHP)
    sf_acs_data = pd.read_csv(SF_ACS_JOIN, dtype={"TL_GEO_ID": "str"})

    # Align geo_id column name in sf_acs_data with GEOID column name in
    # sf_tracts shapefile prior to the merge
    sf_acs_data.rename(columns={"TL_GEO_ID": "GEOID"}, inplace=True)

    updated_sf_tracts = sf_tracts.merge(sf_acs_data, on="GEOID", how="left")
    updated_sf_tracts.to_file(MERGED_SF_TRACTS_SHP)


def generate_zori_csv():
    """
    Loads ZORI CSV file, filters for SF zip codes and the years 2020-2024, imputes
    to fill missing data, and outputs tidy ZORI CSV.

    Returns:
        zips: [list] SF zip codes
    """
    # Load raw data
    df = pd.read_csv("raw-data/zori_by_zip.csv")

    # Filter for San Francisco rows
    sf_zips = df[df["City"] == "San Francisco"].copy()

    # Filter for years of interest: 2020-2024
    date_cols = [
        col
        for col in sf_zips.columns
        if any(yr in col for yr in ["2020", "2021", "2022", "2023", "2024"])
    ]

    filtered_df = sf_zips[["RegionName"] + date_cols]
    filtered_df = filtered_df.rename(columns={"RegionName": "zip"})

    # Imputes data to fill missing values
    zip_col = filtered_df["zip"]
    data = filtered_df.drop(columns=["zip"])
    data = data.interpolate(axis=1)
    data = data.fillna(data.mean())

    imputed_df = pd.concat([zip_col, data], axis=1)

    # Convert into tidy format
    tidy_df = imputed_df.melt(id_vars="zip", var_name="date", value_name="rent")

    # Convert date to standardized format: YYYY-MM
    tidy_df["date"] = pd.to_datetime(tidy_df["date"]).dt.strftime("%Y-%m")
    tidy_df["zip"] = tidy_df["zip"].astype(int).astype(str)

    # Writes tidy CSV
    tidy_df.to_csv("clean-data/tidy_zori.csv", index=False)


def process_crosswalks_xlsx(file_path, zips, tracts):
    """
    Loads crosswalks XLSX file, selects necessary columns (zip, tract, res_ratio),
    filters for specified zips and tracts, and saves date column by extracting
    from filename.

    Parameters:
        file_path: file path for XLSX file
        zips: [set] zips of interest to filter on
        tracts: [set] census tracts of interest to filter on

    Returns:
        filtered_df: Pandas dataframe
    """
    df = pd.read_excel(file_path, engine="openpyxl")
    zip_col = None
    # Pull zip, tract, and res_ratio columns
    for column in df.columns:
        if "zip" in column.lower():
            zip_col = column
            break
    df[zip_col] = df[zip_col].astype(str)
    for column in df.columns:
        if "tract" in column.lower():
            tract_col = column
            break
    df[tract_col] = df[tract_col].astype(str)
    # Ensure tract is 11 characters (add 0 to front as needed)
    df[tract_col] = df[tract_col].str.zfill(11)
    for column in df.columns:
        if "res_ratio" in column.lower():
            res_ratio_col = column
            break
    # Add date column based on filename
    datetime_str = file_path.stem[-6:]
    datetime_object = datetime.strptime(datetime_str, "%m%Y")
    # Convert date to standardized format: YYYY-MM
    date = f"{datetime_object.year}-{datetime_object.month:02}"
    selected_cols_df = df.loc[:, [zip_col, tract_col, res_ratio_col]]
    selected_cols_df["date"] = date
    selected_cols_df.rename(
        columns={"ZIP": "zip", "TRACT": "tract", "RES_RATIO": "res_ratio"},
        inplace=True,
    )
    # Filter to zips of interest
    filtered_by_zips_df = selected_cols_df[selected_cols_df["zip"].isin(zips)]
    # Filter to tracts of interest
    filtered_df = filtered_by_zips_df[filtered_by_zips_df["tract"].isin(tracts)]

    return filtered_df


def generate_crosswalks_csv():
    """
    Cleans multiple crosswalks XLSX files and outputs to a single CSV.
    """
    zori_df = pd.read_csv("clean-data/tidy_zori.csv")
    acs_df = pd.read_csv("clean-data/census_acs_join.csv")

    # Grab SF zips from ZORI data
    zips_num = set(zori_df["zip"])
    sf_zips = {str(zip) for zip in zips_num}

    # Grab SF tracts from census data
    tracts_num = set(acs_df["TL_GEO_ID"])
    short_tracts = {str(tract) for tract in tracts_num}
    sf_tracts = {tract.zfill(11) for tract in short_tracts}

    list_of_dfs = []
    for file_path in Path("raw-data/crosswalks-xlsx").iterdir():
        if not file_path.name.startswith("~$"):
            sf_df = process_crosswalks_xlsx(file_path, sf_zips, sf_tracts)
            list_of_dfs.append(sf_df)

    # Aggregate and output to CSV
    aggregated_df = pd.concat(list_of_dfs)
    aggregated_df.to_csv("clean-data/crosswalks.csv", index=None, header=True)


if __name__ == "__main__":
    process_acs_data()
    create_sf_shapefiles()
    add_sf_tract_data()
    generate_zori_csv()
    generate_crosswalks_csv()
