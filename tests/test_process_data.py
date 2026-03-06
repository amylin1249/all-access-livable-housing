import pandas as pd
from src.process_data import get_sf_geoid
from src.datatypes import SF_CENSUS_PATH, SF_ACS_JOIN


### Add tests on generate encampments and 311 CSVs


def test_get_sf_geoid():
    length_raw_sf_tracts = len(pd.read_csv(SF_CENSUS_PATH))
    assert len(get_sf_geoid()) == length_raw_sf_tracts - 1


def test_process_acs_length():
    length_joined_acs_data = len(pd.read_csv(SF_ACS_JOIN))
    assert length_joined_acs_data == len(get_sf_geoid())


def test_process_acs_impute_neg_rent():
    MEAN_POS_RENT = 2541

    acs_df = pd.read_csv(SF_ACS_JOIN)
    acs_df["TL_GEO_ID"] = acs_df["TL_GEO_ID"].astype(str).str.zfill(11)

    # Test that all tracts which originally had negative rent values have been imputed
    assert acs_df[acs_df["TL_GEO_ID"] == "06075016101"]["med_rent"] == MEAN_POS_RENT
    assert acs_df[acs_df["TL_GEO_ID"] == "06075023200"]["med_rent"] == MEAN_POS_RENT
    assert acs_df[acs_df["TL_GEO_ID"] == "06075031000"]["med_rent"] == MEAN_POS_RENT
    assert acs_df[acs_df["TL_GEO_ID"] == "06075980200"]["med_rent"] == MEAN_POS_RENT


def test_process_acs_impute_neg_income():
    MEAN_POS_INC = 146050

    acs_df = pd.read_csv(SF_ACS_JOIN)
    acs_df["TL_GEO_ID"] = acs_df["TL_GEO_ID"].astype(str).str.zfill(11)

    # Test that all tracts which originally had negative income values have been imputed
    assert acs_df[acs_df["TL_GEO_ID"] == "06075012403"]["med_hh_inc"] == MEAN_POS_INC
    assert acs_df[acs_df["TL_GEO_ID"] == "06075012404"]["med_hh_inc"] == MEAN_POS_INC
    assert acs_df[acs_df["TL_GEO_ID"] == "06075012406"]["med_hh_inc"] == MEAN_POS_INC
    assert acs_df[acs_df["TL_GEO_ID"] == "06075017602"]["med_hh_inc"] == MEAN_POS_INC
    assert acs_df[acs_df["TL_GEO_ID"] == "06075033201"]["med_hh_inc"] == MEAN_POS_INC
    assert acs_df[acs_df["TL_GEO_ID"] == "06075980200"]["med_hh_inc"] == MEAN_POS_INC
    assert acs_df[acs_df["TL_GEO_ID"] == "06075980900"]["med_hh_inc"] == MEAN_POS_INC


def test_process_acs_calc_white_pct():
    MEAN_POS_INC = 146050

    acs_df = pd.read_csv(SF_ACS_JOIN)
    acs_df["TL_GEO_ID"] = acs_df["TL_GEO_ID"].astype(str).str.zfill(11)

    # Test that all tracts which originally had negative income values have been imputed
    assert acs_df[acs_df["TL_GEO_ID"] == "06075012403"]["med_hh_inc"] == MEAN_POS_INC
