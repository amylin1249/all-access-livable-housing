import pandas as pd
import csv
from pathlib import Path
from datetime import datetime

eviction_df = pd.read_csv("clean-data/evictions_api_data_tracts.csv")
acs_df = pd.read_csv("clean-data/census_acs_join.csv")
ENCAMPMENT_DF = pd.read_csv("clean-data/encampment_tracts.csv")
ENCAMPMENT_REPORT_DF = pd.read_csv("clean-data/311_tracts.csv")

TENTS_EST = 1.1
STRUCTURES_EST = 1.1
VEHICLES_EST = 2.1


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
                rent_by_tract[date][tract] += float(
                    rent_by_zip[date][zip_code]
                ) * float(weight)
                weight_sums[date][tract] += float(weight)

    # Division by denominator
    for date in rent_by_tract:
        for tract in rent_by_tract[date]:
            rent_by_tract[date][tract] /= weight_sums[date][tract]

    return rent_by_tract


def encampments_by_tract(df):
    """
    Add docstring
    """
    df["geoid"] = df["geoid"].astype(str).str.zfill(11)
    df["date"] = (
        df["year"].astype(str).str.cat(df["month"].astype(str).str.zfill(2), sep="-")
    )
    ### I think this column "date" should be added under clean_encampment() in process_data.py instead?

    df.groupby(["geoid", "date"], as_index=False).agg(
        {
            "tents": "sum",
            "structures": "sum",
            "vehicles": "sum",
        }
    )

    df = df[["geoid", "date", "tents", "structures", "vehicles"]]

    return df


def generate_tidy_csv(rent_by_tract):
    data = []
    for date, tract_rent in rent_by_tract.items():
        for tract, median_rent in tract_rent.items():
            dict = {}
            dict["date"] = date
            dict["tract"] = tract
            dict["median_rent"] = median_rent
            data.append(dict)

    final_df = pd.DataFrame(data)

    # merge eviction data
    eviction_records = calculate_eviction_rate(eviction_df, acs_df)
    df_evic_list = pd.DataFrame(eviction_records)

    final_df = pd.merge(
        final_df,
        df_evic_list[["year_mon", "geoid", "eviction_rate"]],
        left_on=["date", "tract"],
        right_on=["year_mon", "geoid"],
        how="left",
    )

    final_df["eviction_rate"] = final_df["eviction_rate"].fillna(0)
    final_df = final_df.drop(columns=["year_mon", "geoid"])

    # Merge encampments data with rent data
    encampments_df = encampments_by_tract(ENCAMPMENT_DF)
    encampments_df = encampments_df.rename(columns={"geoid": "tract"})

    final_df = pd.merge(final_df, encampments_df, on=["date", "tract"], how="left")
    final_df = final_df.fillna(0)

    # Calculate weighted estimate of homelessness based on encampment types (rounded)
    final_df["estimate"] = (
        final_df["tents"] * TENTS_EST
        + final_df["structures"] * STRUCTURES_EST
        + final_df["vehicles"] * VEHICLES_EST
    ).round(0)

    final_df.to_csv("clean-data/consolidated_data.csv", index=False)


if __name__ == "__main__":
    TENTS_EST = 1.1
    STRUCTURES_EST = 1.1
    VEHICLES_EST = 2.1

    eviction_df = pd.read_csv("clean-data/evictions_api_data_tracts.csv")
    acs_df = pd.read_csv("clean-data/census_acs_join.csv")
    ENCAMPMENT_DF = pd.read_csv("clean-data/encampment_tracts.csv")

    rent_by_zip = generate_rent_by_zip_dict()
    crosswalks = generate_crosswalks_dict()
    rent_by_tract = weight_to_census_tract(crosswalks, rent_by_zip)

    generate_tidy_csv(rent_by_tract)
