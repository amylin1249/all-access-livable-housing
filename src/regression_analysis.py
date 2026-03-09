##### Data Set up #####
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
import altair as alt
import geopandas as gpd
from pathlib import Path
from datetime import datetime
from .datatypes import (
    CLEAN_311,
    CLEAN_ENCAMP,
    CLEAN_ZILLOW,
    CLEAN_CROSSWALKS,
    JOINED_ENCAMP_TRACTS,
    JOINED_311_TRACTS,
    SF_CENSUS_TRACTS,
    MERGED,
)


def run_reg():

    """
    Runs a regression to understand the relationship between tract features and 
    the unique number of reporte 311 addresses in a month

    Parameters:
        Read in several cleaned data files for process, including joined_encampment_tracts.csv, joined_311_tracts.csv, sf_census_tracts.csv

    Returns:
        RegressionResultsWrapper object, results2, with includes month fixed effects and errors clustered at the tract level
    """
    # Step 1: Load in encampmment-tract crosswalk
    df_crosswalk = pd.read_csv(JOINED_ENCAMP_TRACTS)

    # Step 2: Aggregate up to the quarter date, tract level
    df_crosswalk = (
        df_crosswalk.groupby(["geoid", "date"])[["tents", "structures", "vehicles"]]
        .sum()
        .reset_index()
    )

    # Step 3: Load in 311-tract crosswalk
    df_311_crosswalk = pd.read_csv(JOINED_311_TRACTS)
    # Step 4: Aggregate total encampments over tract and date
    df_311_crosswalk["total_encampments"] = 1
    df_311_crosswalk = (
        df_311_crosswalk.groupby(["geoid", "date"])[["total_encampments"]]
        .sum()
        .reset_index()
    )
    # Step 5: Combine crosswalks on tract and date [this is to get the raw, not interpolated figures, from the 311 file]
    merged_df = pd.merge(
        df_311_crosswalk, df_crosswalk, on=["geoid", "date"], how="inner"
    )
    # Step 6: Load in the ACS data to get demographics
    acs_data = pd.read_csv(SF_CENSUS_TRACTS)
    acs_data = acs_data.rename(columns={"TL_GEO_ID": "geoid"})
    # Step 7: Merge ACS data on the file
    merged_df = pd.merge(merged_df, acs_data, on=["geoid"], how="inner")

    ### Run regressions ####

    # Step 1. Define the OLS model
    model = smf.ols(
        formula="total_encampments ~ med_rent + med_hh_inc + white_pct + C(date)",
        data=merged_df,
    )

    # 2. Fit the model with clustered standard errors
    results = model.fit(cov_type="cluster", cov_kwds={"groups": merged_df["geoid"]})

    # 3. Test with year-month fixed effects
    model2 = smf.ols(
        formula="total_encampments ~ med_rent + med_hh_inc + white_pct  + tents + structures + vehicles + C(date)",
        data=merged_df,
    )
    results2 = model2.fit(cov_type="cluster", cov_kwds={"groups": merged_df["geoid"]})

    return results2
