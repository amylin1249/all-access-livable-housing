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


# Paths to raw encampment counts XLSX and 311 cases CSV
ENCAMP_PATH = Path(__file__).parent.parent / "raw-data/encampment_counts.xlsx"
REPORT_PATH = Path(__file__).parent.parent / "raw-data/311_cases.csv"


# Paths to clean evictions, encampment counts, and 311 cases CSV files
CLEAN_EVICTIONS = Path(__file__).parent.parent / "clean-data/api_evictions_data.csv"
CLEAN_ENCAMP = Path(__file__).parent.parent / "clean-data/clean_encampments_data.csv"
CLEAN_311 = Path(__file__).parent.parent / "clean-data/clean_311_data.csv"


# Paths to clean census CSV file and tract shapefiles
SF_ACS_JOIN = Path(__file__).parent.parent / "clean-data/census_acs_join.csv"
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


# Path to consolidated data file to be used for analysis and visualization
MERGED = Path(__file__).parent.parent / "clean-data/merged_data.csv"


# Column IDs of metrics of interest from raw ACS CSV files
POP_ID = "AUO6E001"
RENT_ID = "AUWGE001"
HH_INC_ID = "AURUE001"
WHITE_POP_ID = "AUO7E002"
RENTER_UNITS_ID = "AUUEE003"
