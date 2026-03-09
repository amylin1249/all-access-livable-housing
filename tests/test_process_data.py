import pandas as pd
import math
from src.process_data import (
    get_sf_geoid,
    clean_address,
)
from src.datatypes import RAW_SF_TRACTS, SF_CENSUS_TRACTS, CLEAN_311, CLEAN_ENCAMP


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
    assert (sum(df_311.duplicated(subset=["date", "lat", "lon"]))) == 0
    assert min(df_311["lat"]) < 38 and min(df_311["lat"]) > 36
    assert min(df_311["date"]) == "2020-01"
    assert max(df_311["date"]) == "2025-01"
    assert min(df_311["lon"]) < -119 and min(df_311["lon"]) > -123


def test_generate_encampments_csv():
    df_encamp = pd.read_csv(CLEAN_ENCAMP)
    assert len(df_encamp) == df_encamp["id"].nunique()
    assert min(df_encamp["lat"]) < 38 and min(df_encamp["lat"]) > 36
    assert min(df_encamp["lon"]) < -119 and min(df_encamp["lon"]) > -123
    assert min(df_encamp["vehicles"]) == 0
    assert min(df_encamp["structures"]) == 0
    assert min(df_encamp["tents"]) == 0
    assert min(df_encamp["date"]) == "2020-01"
    assert max(df_encamp["date"]) == "2025-01"
    # set slightly arbitrary threshold
    assert max(df_encamp["vehicles"]) < 100
    assert max(df_encamp["structures"]) < 100
    assert max(df_encamp["vehicles"]) < 100


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


### Add tests on ZORI
