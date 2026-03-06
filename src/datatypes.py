from pathlib import Path

# Paths to raw ACS CSV files for the relevant metrics
POP_PATH = (
    Path(__file__).parent.parent / "raw-data/census/acs_sf_population_2020_24.csv"
)
RENT_PATH = (
    Path(__file__).parent.parent / "raw-data/census/acs_sf_median_rent_2020_24.csv"
)
HH_INC_PATH = (
    Path(__file__).parent.parent / "raw-data/census/acs_sf_median_hh_income_2020_24.csv"
)
RACE_PATH = Path(__file__).parent.parent / "raw-data/census/acs_sf_race_2020_24.csv"
RENTER_UNITS_PATH = (
    Path(__file__).parent.parent / "raw-data/census/acs_sf_housing_units_2020_24.csv"
)


# Paths to raw SF census tracts CSV file and California tracts shapefiles
SF_CENSUS_PATH = (
    Path(__file__).parent.parent / "raw-data/census/sf_census_tracts_2020.csv"
)
CALI_TRACTS_SHP = (
    Path(__file__).parent.parent
    / "raw-data/census/cali_tracts_shapefiles/tl_2025_06_tract.shp"
)


# Paths to raw encampment counts XLSX and 311 cases CSV
REPORT_PATH = Path(__file__).parent.parent / "raw-data/311_cases.csv"
ENCAMP_PATH = Path(__file__).parent.parent / "raw-data/encampment_counts.xlsx"


# Paths to clean evictions, encampment counts, and 311 cases CSV files
SF_EVICTIONS = Path(__file__).parent.parent / "clean-data/evictions_api_data.csv"
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
SF_EVICTIONS_TRACTS = (
    Path(__file__).parent.parent / "clean-data/evictions_api_data_tracts.csv"
)
ENCAMPMENT_TRACTS = Path(__file__).parent.parent / "clean-data/encampment_tracts.csv"
ENCAMPMENT_REPORT_TRACTS = Path(__file__).parent.parent / "clean-data/311_tracts.csv"


# Path to consolidated data file to be used for analysis and visualization
CONSOLIDATED = Path(__file__).parent.parent / "clean-data/consolidated_data.csv"


# Column IDs of metrics of interest from raw ACS CSV files
POP_ID = "AUO6E001"
RENT_ID = "AUWGE001"
HH_INC_ID = "AURUE001"
WHITE_POP_ID = "AUO7E002"
RENTER_UNITS_ID = "AUUEE003"
