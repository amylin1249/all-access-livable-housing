import pandas as pd
import csv
from pathlib import Path
from datetime import datetime

eviction_df = pd.read_csv("clean-data/evictions_api_data_tracts.csv")
acs_df = pd.read_csv("clean-data/census_acs_join.csv")

def total_evictions_by_tract(eviction_df):
    """
    Combine current evictions data with census tracts 
    to get total number of evictions within a tract for a given month
    """
    
    eviction_df["geoid"] = eviction_df['geoid'].astype(str).str.zfill(11)
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
    acs_df["TL_GEO_ID"] = acs_df['TL_GEO_ID'].astype(str).str.zfill(11)

    merged = pd.merge(
        agg_eviction_df, 
        acs_df[['TL_GEO_ID', 'rent_units']], 
        left_on='geoid', 
        right_on='TL_GEO_ID', 
        how='left'
    )
    merged['eviction_rate'] = merged['total_evictions'] / merged['rent_units']
    merged['eviction_rate'] = merged['eviction_rate'].fillna(0)

    return merged.to_dict(orient='records')


def generate_rent_by_zip_dict():
    rent_by_zip = {}

    with open("clean-data/tidy_zori.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["date"] not in rent_by_zip:
                rent_by_zip[row["date"]] = {}
            if row["zip"] not in rent_by_zip[row["date"]]:
                rent_by_zip[row["date"]][row["zip"]] = row["rent"]  

    return rent_by_zip


def generate_crosswalks_dict():
    """
    crosswalks: [dict] monthly crosswalk data per SF zip code, with 
        (tract, res_ratio)
    """
    # Generate dictionary with crosswalks data
    crosswalks = {}
    with open("clean-data/crosswalks.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["date"] not in crosswalks:
                crosswalks[row["date"]] = {}
            if row["zip"] not in crosswalks[row["date"]]:
                crosswalks[row["date"]][row["zip"]] = []
            crosswalks[row["date"]][row["zip"]].append((row["tract"], row["res_ratio"]))
    
    # Fill in missing months (e.g., March 2020 --> Jan 2020, Feb 2020, and March 2020)
    ### TECHNICALLY COULD INTERPOLATE? BUT SEEMS UNNECESSARY
    for year in range(2020, 2025):
        for month in range(1, 13):
            current_date = f"{year}-{month:02}"
            if current_date not in crosswalks:
                if month <= 3:
                    crosswalks[current_date] = crosswalks[f"{year}-03"]
                elif month <= 6:
                    crosswalks[current_date] = crosswalks[f"{year}-06"]
                elif month <= 9:
                    crosswalks[current_date] = crosswalks[f"{year}-09"]
                else:
                    crosswalks[current_date] = crosswalks[f"{year}-12"]
    
    return crosswalks


def weight_to_census_tract(crosswalks, rent_by_zip):
    rent_by_tract = {}
    # Denominator
    weight_sums = {}

    # Generate numerator (sum of weight * rent) and denominator (sum of weights)
    for date in crosswalks:
        for zip_code in crosswalks[date]:
            for tract, weight in crosswalks[date][zip_code]:
                if date not in rent_by_tract:
                    rent_by_tract[date] = {}
                    weight_sums[date] = {}
                if tract not in rent_by_tract[date]:
                    rent_by_tract[date][tract] = 0
                    weight_sums[date][tract] = 0
                rent_by_tract[date][tract] += float(rent_by_zip[date][zip_code]) * float(weight)
                weight_sums[date][tract] += float(weight)

    # Division by denominator
    for date in rent_by_tract:
        for tract in rent_by_tract[date]:
            rent_by_tract[date][tract] /= weight_sums[date][tract]

    return rent_by_tract


def generate_tidy_csv(rent_by_tract):
    # This doesn't work here
    # df = pd.DataFrame.from_dict(rent_by_tract, orient='columns')
    # df.to_csv('FINAL-DATA.csv')


if __name__ == "__main__":
    rent_by_zip = generate_rent_by_zip_dict()
    crosswalks = generate_crosswalks_dict()
    rent_by_tract = weight_to_census_tract(crosswalks, rent_by_zip)
    generate_tidy_csv(rent_by_tract)
