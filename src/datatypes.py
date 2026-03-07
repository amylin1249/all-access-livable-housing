from pathlib import Path

# Paths to raw ACS CSV files for the relevant metrics
RAW_ACS_POP = (
    Path(__file__).parent.parent / "raw-data/census/raw_acs_sf_population_2020_24.csv"
)
RAW_ACS_RENT = (
    Path(__file__).parent.parent / "raw-data/census/raw_acs_sf_median_rent_2020_24.csv"
)
RAW_ACS_HH_INC = (
    Path(__file__).parent.parent / "raw-data/census/raw_acs_sf_median_hh_income_2020_24.csv"
)
RAW_ACS_RACE = Path(__file__).parent.parent / "raw-data/census/raw_acs_sf_race_2020_24.csv"
RAW_ACS_RENTER_UNITS = (
    Path(__file__).parent.parent / "raw-data/census/raw_acs_sf_housing_units_2020_24.csv"
)


# Paths to raw SF census tracts CSV file and California tracts shapefiles
RAW_SF_TRACTS = (
    Path(__file__).parent.parent / "raw-data/census/raw_sf_census_tracts_2020.csv"
)
CALI_TRACTS_SHP = (
    Path(__file__).parent.parent
    / "raw-data/census/cali_tracts_shapefiles/tl_2025_06_tract.shp"
)


# Paths to raw encampment counts XLSX, 311 cases CSV, and Zillow CSV
RAW_ENCAMP = Path(__file__).parent.parent / "raw-data/raw_encampments_data.xlsx"
RAW_311 = Path(__file__).parent.parent / "raw-data/raw_311_data.csv"
RAW_ZILLOW = Path(__file__).parent.parent / "raw-data/raw_zillow_data.csv"

# Path to raw crosswalks XLSX files folder
RAW_CROSSWALKS = Path(__file__).parent.parent / "raw-data/raw_crosswalks"

# Paths to clean evictions, encampment counts, 311 cases, Zillow, and crosswalks CSV files
CLEAN_EVICTIONS = Path(__file__).parent.parent / "clean-data/api_evictions_data.csv"
CLEAN_ENCAMP = Path(__file__).parent.parent / "clean-data/clean_encampments_data.csv"
CLEAN_311 = Path(__file__).parent.parent / "clean-data/clean_311_data.csv"
CLEAN_ZILLOW = Path(__file__).parent.parent / "clean-data/clean_311_zillow_data.csv"
CLEAN_CROSSWALKS = Path(__file__).parent.parent / "clean-data/clean_crosswalks.csv"


# Paths to clean census CSV file and tract shapefiles
SF_CENSUS_TRACTS = Path(__file__).parent.parent / "clean-data/sf_census_tracts.csv"
SF_TRACTS_SHP = Path(__file__).parent.parent / "clean-data/sf_shapefiles/sf_tracts.shp"
MERGED_SF_TRACTS_SHP = (
    Path(__file__).parent.parent
    / "clean-data/merged_sf_shapefiles/merged_sf_tracts.shp"
)


# Paths to CSV files with point data that have been spatially matched with tracts
JOINED_EVICTIONS_TRACTS = (
    Path(__file__).parent.parent / "clean-data/joined_evictions_tracts.csv"
)
JOINED_ENCAMP_TRACTS = Path(__file__).parent.parent / "clean-data/joined_encampment_tracts.csv"
JOINED_311_TRACTS = Path(__file__).parent.parent / "clean-data/joined_311_tracts.csv"


# Path to consolidated/merged data file to be used for analysis and visualization
MERGED = Path(__file__).parent.parent / "clean-data/merged_data.csv"


# Column IDs of metrics of interest from raw ACS CSV files
ACS_POP_ID = "AUO6E001"
ACS_RENT_ID = "AUWGE001"
ACS_HH_INC_ID = "AURUE001"
ACS_WHITE_POP_ID = "AUO7E002"
ACS_RENTER_UNITS_ID = "AUUEE003"
