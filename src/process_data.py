import csv
import sys
import pandas as pd
import geopandas as gpd
from pathlib import Path
from datetime import datetime
from .datatypes import (
    RAW_SF_TRACTS,
    RAW_ACS_POP,
    RAW_ACS_RENT,
    RAW_ACS_HH_INC,
    RAW_ACS_RACE,
    RAW_ACS_RENTER_UNITS,
    ACS_POP_ID,
    ACS_RENT_ID,
    ACS_HH_INC_ID,
    ACS_WHITE_POP_ID,
    ACS_RENTER_UNITS_ID,
    SF_CENSUS_TRACTS,
    CALI_TRACTS_SHP,
    SF_TRACTS_SHP,
    MERGED_SF_TRACTS_SHP,
    RAW_311,
    CLEAN_311,
    RAW_ENCAMP,
    CLEAN_ENCAMP,
    RAW_ZILLOW,
    RAW_CROSSWALKS,
    CLEAN_ZILLOW,
    CLEAN_CROSSWALKS,
)

EXCLUDE_GEOID = "06075980401"

SF_TRACTS_DIR = Path(__file__).parent.parent / "clean-data/sf_shapefiles"
MERGED_SF_TRACTS_DIR = Path(__file__).parent.parent / "clean-data/merged_sf_shapefiles"

def get_sf_geoid() -> list[str]:
    """
    Extract the list of SF census tract GeoIDs based on the list of 2020 census
    tracts from DataSF Open Data Portal, removing any tracts to be excluded.

    Returns:
        List of filtered SF census tract GeoIDs.
    """
    sf_geoid = []

    csv.field_size_limit(sys.maxsize)

    with open(RAW_SF_TRACTS) as f:
        reader = csv.DictReader(f)
        for row in reader:
            geoid = row["geoid"]
            if geoid != EXCLUDE_GEOID:
                sf_geoid.append(geoid)

    return sf_geoid


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
        RAW_ACS_POP, usecols=["TL_GEO_ID", ACS_POP_ID], dtype={"TL_GEO_ID": "str"}
    )
    race_df = pd.read_csv(
        RAW_ACS_RACE,
        usecols=["TL_GEO_ID", ACS_WHITE_POP_ID],
        dtype={"TL_GEO_ID": "str"},
    )
    rent_df = pd.read_csv(
        RAW_ACS_RENT, usecols=["TL_GEO_ID", ACS_RENT_ID], dtype={"TL_GEO_ID": "str"}
    )
    hh_inc_df = pd.read_csv(
        RAW_ACS_HH_INC, usecols=["TL_GEO_ID", ACS_HH_INC_ID], dtype={"TL_GEO_ID": "str"}
    )
    renter_df = pd.read_csv(
        RAW_ACS_RENTER_UNITS,
        usecols=["TL_GEO_ID", ACS_RENTER_UNITS_ID],
        dtype={"TL_GEO_ID": "str"},
    )

    # Impute negative values (i.e., missing) in rent and household income
    # dataframes with the mean of their positive values
    mean_rent = round(rent_df.loc[rent_df[ACS_RENT_ID] > 0, ACS_RENT_ID].mean())
    rent_df.loc[rent_df[ACS_RENT_ID] < 0, ACS_RENT_ID] = mean_rent

    mean_hh_inc = round(
        hh_inc_df.loc[hh_inc_df[ACS_HH_INC_ID] > 0, ACS_HH_INC_ID].mean()
    )
    hh_inc_df.loc[hh_inc_df[ACS_HH_INC_ID] < 0, ACS_HH_INC_ID] = mean_hh_inc

    # Merge individual dataframes based on GEO_ID
    joined_df = pop_df
    for df in [race_df, rent_df, hh_inc_df, renter_df]:
        joined_df = pd.merge(joined_df, df, on="TL_GEO_ID", how="left")

    # Rename population, race, rent, income, and renter units column names
    joined_df = joined_df.rename(
        columns={
            ACS_POP_ID: "population",
            ACS_WHITE_POP_ID: "white_pop",
            ACS_RENT_ID: "med_rent",
            ACS_HH_INC_ID: "med_hh_inc",
            ACS_RENTER_UNITS_ID: "rent_units",
        }
    )

    # Add calculation of percentage of white population per tract as a new column
    joined_df["white_pct"] = joined_df["white_pop"] / joined_df["population"]

    # Filter tract IDs only for those in the list of filtered SF census tracts
    joined_df = joined_df[joined_df["TL_GEO_ID"].isin(get_sf_geoid())]

    joined_df.to_csv(SF_CENSUS_TRACTS, index=False)


def create_sf_shapefiles():
    """
    Filter California census tract shapefiles and create SF census tract
    shapefiles that only include tracts in San Francisco, by matching with the
    GeoIDs obtained from the San Francisco list of census tracts.
    """
    cali_tracts = gpd.read_file(CALI_TRACTS_SHP)

    # Filter California tract IDs only for those that are in SF
    sf_tracts = cali_tracts[cali_tracts["GEOID"].isin(get_sf_geoid())]

    if not SF_TRACTS_DIR.exists():
        SF_TRACTS_DIR.mkdir()

    sf_tracts.to_file(SF_TRACTS_SHP)


def add_sf_tract_data():
    """
    Add SF ACS data to SF census tract shapefiles as attributes, and save to new
    SF census tract shapefiles containing the merged attributes.
    """
    sf_tracts = gpd.read_file(SF_TRACTS_SHP)
    sf_acs_data = pd.read_csv(SF_CENSUS_TRACTS, dtype={"TL_GEO_ID": "str"})

    # Align geo_id column name in sf_acs_data with GEOID column name in
    # sf_tracts shapefile prior to the merge
    sf_acs_data.rename(columns={"TL_GEO_ID": "GEOID"}, inplace=True)

    updated_sf_tracts = sf_tracts.merge(sf_acs_data, on="GEOID", how="left")

    if not MERGED_SF_TRACTS_DIR.exists():
        MERGED_SF_TRACTS_DIR.mkdir()

    updated_sf_tracts.to_file(MERGED_SF_TRACTS_SHP)


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


def clean_parenthesis(phrase: str) -> str:
    """
    This function takes a phrase and removes any parenthesized portion.

    Parameters:
        phrase: a string representing a phrase

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
    """
    ADD DOCSTRING
    """
    address = address.lower()
    address = address.replace("i poi", "")
    address = clean_parenthesis(address)
    text_data = address.split(" ")
    cleaned_list = [word.strip(PUNCTUATION) for word in text_data]
    cleaned_list = [word for word in cleaned_list if word != ""]
    cleaned_list = [word for word in cleaned_list if word not in STOPWORDS]
    return " ".join(cleaned_list)


def generate_311_csv():
    """
    ADD DOCSTRING
    """
    # Load raw data
    df = pd.read_csv(RAW_311)

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

    # Drop observations where lat/lon = 0
    df = df[(df["lat"] != 0) & (df["lon"] != 0)]

    # Reorder columns for readability
    df = df.reindex(columns=["id", "date", "lat", "lon"])

    df.to_csv(CLEAN_311, index=False)


def generate_encampments_csv():
    """
    ADD DOCSTRING
    """
    # Top row (row 0) is not a real header row
    df = pd.read_excel(RAW_ENCAMP, header=1)

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

    df.to_csv(CLEAN_ENCAMP, index=False)


def generate_zillow_csv():
    """
    Loads Zillow CSV file, filters for SF zip codes and the years 2020-2024, imputes
    to fill missing data, and outputs tidy Zillow CSV.

    Returns:
        zips: [list] SF zip codes
    """
    # Load raw data
    df = pd.read_csv(RAW_ZILLOW)

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
    tidy_df.to_csv(CLEAN_ZILLOW, index=False)


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
    zillow_df = pd.read_csv(CLEAN_ZILLOW)
    tracts_df = pd.read_csv(SF_CENSUS_TRACTS)

    # Grab SF zips from Zillow data
    zips_num = set(zillow_df["zip"])
    sf_zips = {str(zip) for zip in zips_num}

    # Grab SF tracts from census data
    tracts_num = set(tracts_df["TL_GEO_ID"])
    short_tracts = {str(tract) for tract in tracts_num}
    sf_tracts = {tract.zfill(11) for tract in short_tracts}

    list_of_dfs = []
    for file_path in Path(RAW_CROSSWALKS).iterdir():
        # Skip over hidden/system/temp files
        if not file_path.name.startswith(("~$", "_$", ".")):
            sf_df = process_crosswalks_xlsx(file_path, sf_zips, sf_tracts)
            list_of_dfs.append(sf_df)

    # Aggregate and output to CSV
    aggregated_df = pd.concat(list_of_dfs)
    aggregated_df.to_csv(CLEAN_CROSSWALKS, index=None, header=True)


if __name__ == "__main__":
    process_acs_data()
    create_sf_shapefiles()
    add_sf_tract_data()
    generate_311_csv()
    generate_encampments_csv()
    generate_zillow_csv()
    generate_crosswalks_csv()
