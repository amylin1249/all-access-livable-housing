import math
import pandas as pd
from src.process_data import (
    get_sf_geoid,
    clean_address,
)
from src.datatypes import (
    RAW_SF_TRACTS,
    SF_CENSUS_TRACTS,
    CLEAN_311,
    CLEAN_ENCAMP,
    CLEAN_ZILLOW,
    CLEAN_CROSSWALKS,
)


def test_clean_address():
    assert clean_address("Intersection of ALABAMA ST and 15TH ST") == "alabama 15th"
    assert (
        clean_address("Intersection of CESAR CHAVEZ ST and HWY 101 N ON RAMP")
        == "cesar chavez hwy 101 n ramp"
    )
    assert clean_address("Intersection of ELM ST and END (200 BLOCK OF)") == "elm end"
    assert (
        clean_address("1499 POTRERO AVE, SAN FRANCISCO, CA, 94110")
        == "1499 potrero san francisco ca 94110"
    )
    assert clean_address("the cliff(f(google) and the .. street") == "cliff"
    assert clean_address("? street i poi 45 yellow") == "45 yellow"


def test_generate_311_csv():
    df_311 = pd.read_csv(CLEAN_311)
    assert len(df_311) == df_311["id"].nunique()
    assert (sum(df_311.duplicated(subset=["date", "lat", "lon"]))) == 0
    assert (df_311["lat"] >= 36).all()
    assert (df_311["lat"] <= 38).all()
    assert (df_311["lon"] >= -123).all()
    assert (df_311["lon"] <= -119).all()
    assert min(df_311["date"]) == "2020-01"
    assert max(df_311["date"]) == "2024-12"


def test_generate_encampments_csv():
    df_encamp = pd.read_csv(CLEAN_ENCAMP)
    assert len(df_encamp) == df_encamp["id"].nunique()
    assert df_encamp["lat"].between(36, 38).all()
    assert df_encamp["lon"].between(-123, -119).all()
    assert min(df_encamp["vehicles"]) == 0
    assert min(df_encamp["structures"]) == 0
    assert min(df_encamp["tents"]) == 0
    assert min(df_encamp["date"]) == "2020-01"
    assert max(df_encamp["date"]) == "2025-01"
    # set slightly arbitrary threshold
    assert max(df_encamp["vehicles"]) < 100
    assert max(df_encamp["structures"]) < 100
    assert max(df_encamp["tents"]) < 100


def test_generate_zillow_csv():
    df_zillow = pd.read_csv(CLEAN_ZILLOW)

    # Test start and end date
    assert df_zillow["date"].min() == "2020-01"
    assert df_zillow["date"].max() == "2024-12"

    # Test rent values are numeric and non-negative
    assert pd.api.types.is_numeric_dtype(df_zillow["rent"])
    assert (df_zillow["rent"] >= 0).all()

    # Test rent is in reasonable range
    assert df_zillow["rent"].max() < 6000
    assert df_zillow["rent"].min() > 0


def test_generate_crosswalks_csv():
    df_crosswalks = pd.read_csv(CLEAN_CROSSWALKS)

    # Test expected columns exist
    expected_columns = {"zip", "tract", "res_ratio", "date"}
    assert set(df_crosswalks.columns) == expected_columns

    # Test start and end date (quarterly crosswalks)
    assert df_crosswalks["date"].min() == "2020-03"
    assert df_crosswalks["date"].max() == "2024-12"

    # Test res_ratio is in reasonable range
    assert df_crosswalks["res_ratio"].min() >= 0
    assert df_crosswalks["res_ratio"].max() <= 1

    # Test each zip, tract pair has exactly 20 rows (quarterly data for 5 years)
    counts_per_pair = df_crosswalks.groupby(["zip", "tract"]).size()
    assert (counts_per_pair == 20).all()


ACS_DF = pd.read_csv(SF_CENSUS_TRACTS)
ACS_DF["TL_GEO_ID"] = ACS_DF["TL_GEO_ID"].astype(str).str.zfill(11)


def test_get_sf_geoid():
    length_raw_sf_tracts = len(pd.read_csv(RAW_SF_TRACTS))
    assert len(get_sf_geoid()) == length_raw_sf_tracts - 1


def test_process_acs_length():
    length_joined_acs_data = len(ACS_DF)
    assert length_joined_acs_data == len(get_sf_geoid())


def test_process_acs_impute_neg_rent():
    MEAN_POS_RENT = 2541

    # Test that all tracts which originally had negative rent values have been imputed
    assert (
        ACS_DF[ACS_DF["TL_GEO_ID"] == "06075016101"]["med_rent"].item() == MEAN_POS_RENT
    )
    assert (
        ACS_DF[ACS_DF["TL_GEO_ID"] == "06075023200"]["med_rent"].item() == MEAN_POS_RENT
    )
    assert (
        ACS_DF[ACS_DF["TL_GEO_ID"] == "06075031000"]["med_rent"].item() == MEAN_POS_RENT
    )
    assert (
        ACS_DF[ACS_DF["TL_GEO_ID"] == "06075980200"]["med_rent"].item() == MEAN_POS_RENT
    )


def test_process_acs_impute_neg_income():
    MEAN_POS_INC = 146050

    # Test that all tracts which originally had negative income values have been imputed
    assert (
        ACS_DF[ACS_DF["TL_GEO_ID"] == "06075012403"]["med_hh_inc"].item()
        == MEAN_POS_INC
    )
    assert (
        ACS_DF[ACS_DF["TL_GEO_ID"] == "06075012404"]["med_hh_inc"].item()
        == MEAN_POS_INC
    )
    assert (
        ACS_DF[ACS_DF["TL_GEO_ID"] == "06075012406"]["med_hh_inc"].item()
        == MEAN_POS_INC
    )
    assert (
        ACS_DF[ACS_DF["TL_GEO_ID"] == "06075017602"]["med_hh_inc"].item()
        == MEAN_POS_INC
    )
    assert (
        ACS_DF[ACS_DF["TL_GEO_ID"] == "06075033201"]["med_hh_inc"].item()
        == MEAN_POS_INC
    )
    assert (
        ACS_DF[ACS_DF["TL_GEO_ID"] == "06075980200"]["med_hh_inc"].item()
        == MEAN_POS_INC
    )
    assert (
        ACS_DF[ACS_DF["TL_GEO_ID"] == "06075980900"]["med_hh_inc"].item()
        == MEAN_POS_INC
    )


def test_process_acs_calc_white_pct():
    # Test calculations of white_pct of select tracts by dividing white_pop by population
    assert math.isclose(
        ACS_DF[ACS_DF["TL_GEO_ID"] == "06075010702"]["white_pct"].item(), 423 / 1398
    )
    assert math.isclose(
        ACS_DF[ACS_DF["TL_GEO_ID"] == "06075012902"]["white_pct"].item(), 1810 / 2589
    )
    assert math.isclose(
        ACS_DF[ACS_DF["TL_GEO_ID"] == "06075026201"]["white_pct"].item(), 366 / 3856
    )
