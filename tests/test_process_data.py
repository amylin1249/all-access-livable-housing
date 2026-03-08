import pandas as pd
import math
from src.process_data import get_sf_geoid
from src.datatypes import RAW_SF_TRACTS, SF_CENSUS_TRACTS


### Add tests on generate encampments and 311 CSVs

## Tests for Lily to add on encampments and 311 CSVs

## Ensure your cleaned dataset has the expected columns.
## Verify cleaning removed or handled nulls.
## Ensure values fall in expected ranges.clean_df["value"].between(0, 100).all()
## Duplicate Checks
## Row count checks
## can test particular values





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
