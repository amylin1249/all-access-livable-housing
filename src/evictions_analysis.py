import pandas as pd

def aggregate_evictions_by_tract(eviction_df):
    """
    Combine current evictions data with census tracts 
    to get total number of evictions within a tract for a given month
    """

    eviction_df = pd.read_csv("clean-data/evictions_api_data_tracts.csv")
    eviction_df["geoid"] = eviction_df['geoid'].astype(str).str.zfill(11)
    group_by_month = eviction_df.groupby(["geoid", "year_mon"])
    counts = group_by_month.size()



def eviction_rate():
    """
    Divide total number of evictions within a tract for a given month 
    by avg monthly num renter hh to get evictions rate
    return eviction_mon / renter_hh
    """
    eviction_df = pd.read_csv("clean-data/evictions_api_data_tracts.csv", dtype={'geoid': str})
    
    for 
    rate = eviction_df["total_evictions"] / eviction_df["renter_hh"]

   
    return 
