import pandas as pd


eviction_df = pd.read_csv("clean-data/evictions_api_data_tracts.csv")
acs_df = pd.read_csv("clean-data/census_acs_join.csv")


def total_evictions_by_tract(eviction_df):
    """
    Combine current evictions data with census tracts
    to get total number of evictions within a tract for a given month
    """

    eviction_df["geoid"] = eviction_df["geoid"].astype(str).str.zfill(11)
    group_by_month = eviction_df.groupby(["geoid", "year_mon"])
    total_evic_per_mon = group_by_month.size().reset_index(name="total_evictions")

    return total_evic_per_mon


def calculate_eviction_rate(eviction_df, acs_df):
    """
    Divide total number of evictions within a tract for a given month
    by avg monthly num renter hh to get evictions rate
    return eviction_mon / rent_units
    """
    agg_eviction_df = total_evictions_by_tract(eviction_df)
    acs_df["TL_GEO_ID"] = acs_df["TL_GEO_ID"].astype(str).str.zfill(11)

    merged = pd.merge(
        agg_eviction_df,
        acs_df[["TL_GEO_ID", "rent_units"]],
        left_on="geoid",
        right_on="TL_GEO_ID",
        how="left",
    )
    merged["eviction_rate"] = merged["total_evictions"] / merged["rent_units"]
    merged["eviction_rate"] = merged["eviction_rate"].fillna(0)

    return merged.to_dict(orient="records")
