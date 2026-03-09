import pandas as pd
import statsmodels.formula.api as smf
from .datatypes import (
    JOINED_ENCAMP_TRACTS,
    JOINED_311_TRACTS,
    SF_CENSUS_TRACTS,
)


def run_reg():
    """
    Runs a regression to understand the relationship between tract features and
    the unique number of reported 311 addresses in a given month witih available point estimates

    Parameters:
        Read in several cleaned data files for process, including
        joined_encampment_tracts.csv, joined_311_tracts.csv, sf_census_tracts.csv

    Returns:
        RegressionResultsWrapper object, results2, with includes month fixed
        effects and errors clustered at the tract level
    """
    # Load encampmment-tract crosswalk data and aggregate by tract and date
    df_crosswalk = pd.read_csv(JOINED_ENCAMP_TRACTS)
    df_crosswalk = (
        df_crosswalk.groupby(["geoid", "date"])[["tents", "structures", "vehicles"]]
        .sum()
        .reset_index()
    )

    # Load 311-tract crosswalk data and aggregate by tract and date
    df_311_crosswalk = pd.read_csv(JOINED_311_TRACTS)
    df_311_crosswalk["total_encampments"] = 1
    df_311_crosswalk = (
        df_311_crosswalk.groupby(["geoid", "date"])[["total_encampments"]]
        .sum()
        .reset_index()
    )

    # Combine crosswalks on tract and date to get the raw, not interpolated
    # figures, from the 311 file
    merged_df = pd.merge(
        df_311_crosswalk, df_crosswalk, on=["geoid", "date"], how="inner"
    )

    # Load ACS data to get demographics and merge with consolidated file
    acs_data = pd.read_csv(SF_CENSUS_TRACTS)
    acs_data = acs_data.rename(columns={"TL_GEO_ID": "geoid"})
    merged_df = pd.merge(merged_df, acs_data, on=["geoid"], how="inner")

    # Run regression, define OLS model, and test with year-month fixed effects
    model2 = smf.ols(
        formula="total_encampments ~ med_rent + med_hh_inc + white_pct  + tents + structures + vehicles + C(date)",
        data=merged_df,
    )
    results2 = model2.fit(cov_type="cluster", cov_kwds={"groups": merged_df["geoid"]})

    return results2
