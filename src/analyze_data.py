import csv
import pandas as pd

from .datatypes import (
    CLEAN_ZILLOW,
    CLEAN_CROSSWALKS,
    JOINED_EVICTIONS_TRACTS,
    SF_CENSUS_TRACTS,
    JOINED_ENCAMP_TRACTS,
    JOINED_311_TRACTS,
    MERGED,
)


# Multipliers from Sacramento 2024 PIT Report
TENTS_EST = 1.9
STRUCTURES_EST = 1.7
VEHICLES_EST = 1.6


def generate_rent_by_zip_dict() -> dict[str, dict[str, float]]:
    """
    Generates the median monthly rent for each SF zip code.

    Returns:
        A dictionary mapping each month to zip code level rents.
    """
    rent_by_zip = {}

    with open(CLEAN_ZILLOW) as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = row["date"]
            zip_code = row["zip"]
            rent = float(row["rent"])
            if date not in rent_by_zip:
                rent_by_zip[date] = {}
            rent_by_zip[date][zip_code] = rent

    return rent_by_zip


def generate_crosswalks_dict() -> dict[str, dict[str, list[tuple[str, float]]]]:
    """
    Generates percentage contribution of a tract's population to the zip code's
    population for a given month.

    Returns:
        A dictionary of monthly crosswalk data (tract's population contribution)
        for each SF zip code, where each value is a list of (tract, res_ratio) tuples.
    """
    crosswalks = {}

    with open(CLEAN_CROSSWALKS) as f:
        reader = csv.DictReader(f)
        for row in reader:
            for row in reader:
                date = row["date"]
                zip_code = row["zip"]
                tract = row["tract"]
                res_ratio = float(row["res_ratio"])
                if date not in crosswalks:
                    crosswalks[date] = {}
                if zip_code not in crosswalks[date]:
                    crosswalks[date][zip_code] = []
                crosswalks[date][zip_code].append((tract, res_ratio))

    # Fill in missing months (e.g., March 2020 --> Jan 2020, Feb 2020, and March 2020)
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


def weight_to_census_tract(
    crosswalks: dict, rent_by_zip: dict
) -> dict[str, dict[str, float]]:
    """
    Estimate monthly census tract level rents by applying crosswalk weights to
    monthly ZIP code level rent data.

    Inputs:
        crosswalks: a dictionary of monthly crosswalk data
        rent_by_zip: a dictionary mapping each month to zip code level rents

    Returns:
        A dictionary with estimated median rent for each census tract by month.
    """
    rent_by_tract = {}
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
                rent_by_tract[date][tract] += rent_by_zip[date][zip_code] * weight
                weight_sums[date][tract] += weight

    # Divide numerator by denominator (compute weighted average rent)
    for date in rent_by_tract:
        for tract in rent_by_tract[date]:
            rent_by_tract[date][tract] /= weight_sums[date][tract]

    return rent_by_tract


def generate_acs_df() -> pd.DataFrame:
    """
    Convert SF census tracts' ACS data from CSV to DataFrame.

    Returns:
        A pandas.DataFrame object with SF census tracts' ACS data.
    """
    acs_df = pd.read_csv(SF_CENSUS_TRACTS)
    acs_df["TL_GEO_ID"] = acs_df["TL_GEO_ID"].astype(str).str.zfill(11)

    return acs_df


def count_evictions_by_tract() -> pd.DataFrame:
    """
    Aggregate number of evictions in each tract and month.

    Returns:
        A pandas.DataFrame object aggregating the number of evictions by tract
        and month.
    """
    evictions_df = pd.read_csv(JOINED_EVICTIONS_TRACTS)

    evictions_df["geoid"] = evictions_df["geoid"].astype(str).str.zfill(11)
    group_by_month = evictions_df.groupby(["geoid", "year_mon"])
    evictions_per_month = group_by_month.size().reset_index(name="total_evictions")

    return evictions_per_month


def calculate_eviction_rate() -> list[dict]:
    """
    Calculate eviction rates for each tract and month, defined as the number of
    evictions in a tract/month divided by the number of renter-occupied housing
    units in that tract from the census.

    Returns:
        A list of dictionaries containing tract, month, total evictions,
        renter units, and the calculated eviction rate.
    """
    acs_df = generate_acs_df()
    agg_eviction_df = count_evictions_by_tract()

    merged = pd.merge(
        agg_eviction_df,
        acs_df[["TL_GEO_ID", "rent_units"]],
        left_on="geoid",
        right_on="TL_GEO_ID",
        how="left",
    )
    merged["geoid"] = merged["TL_GEO_ID"]
    merged["eviction_rate"] = merged["total_evictions"] / merged["rent_units"]

    return merged.to_dict(orient="records")


def count_311_by_tract() -> pd.DataFrame:
    """
    Aggregate number of 311 calls in each tract and month.

    Returns:
        A pandas.DataFrame object aggregating the number of 311 calls by tract
        and month
    """
    df = pd.read_csv(JOINED_311_TRACTS)
    df["geoid"] = df["geoid"].astype(str).str.zfill(11)

    return df.groupby(["geoid", "date"]).size().reset_index(name="311_calls")


def count_encampments_by_tract() -> pd.DataFrame:
    """
    Aggregate number of encampments (tents, structures, vehicles) in each tract
    and month.

    Returns:
        A pandas.DataFrame object aggregating the number of encampments by tract
        and month
    """
    df = pd.read_csv(JOINED_ENCAMP_TRACTS)
    df["geoid"] = df["geoid"].astype(str).str.zfill(11)

    return df.groupby(["geoid", "date"], as_index=False).agg(
        {
            "tents": "sum",
            "structures": "sum",
            "vehicles": "sum",
        }
    )


def generate_tidy_csv():
    """
    Integrating multi-source housing and homelessness datasets into a unified
    tidy CSV for tract-level analysis.

    This function executes the core data engineering pipeline:
    1. Crosswalks ZIP-level ZORI rent data to Census Tracts and applies ACS-based
       scaling factors to adjust for local median rent variations.
    2. Merges calculated eviction rates and aggregates 311 encampment-related
       service calls by tract and month.
    3. Processes quarterly encampment point-in-time counts by performing linear
       interpolation to generate monthly estimates (tents, structures, and vehicles).
    4. Calculates a weighted homelessness estimate using predefined conservative
       multipliers for different encampment types.
    5. Exports the final integrated dataset to a 'merged' CSV file for
       downstream visualization and regression analysis.

    Returns:
        None: Saves the processed DataFrame to the path specified by the
        MERGED constant
    """
    acs_df = generate_acs_df()

    # Convert monthly median rent per SF census tract dictionary into rows of tidy CSV
    rent_by_zip = generate_rent_by_zip_dict()
    crosswalks = generate_crosswalks_dict()
    rent_by_tract = weight_to_census_tract(crosswalks, rent_by_zip)

    data = []
    for date, tract_rent in rent_by_tract.items():
        for tract, median_rent in tract_rent.items():
            row_dict = {}
            row_dict["date"] = date
            row_dict["tract"] = tract
            row_dict["median_rent"] = median_rent
            data.append(row_dict)

    tidy_df = pd.DataFrame(data)

    census_tracts = tidy_df["tract"].unique()

    # Scale calculated monthly median rent by census median rent value (one value
    # for 2020-2024)
    for tract in census_tracts:
        tract_rows = tidy_df["tract"] == tract
        avg_rent = tidy_df.loc[tract_rows, "median_rent"].mean()
        scaling_factor = (
            acs_df.loc[acs_df["TL_GEO_ID"] == tract, "med_rent"].item() / avg_rent
        )
        tidy_df.loc[tract_rows, "median_rent"] *= scaling_factor

    # Merge eviction data
    eviction_records = calculate_eviction_rate()
    df_evic_list = pd.DataFrame(eviction_records)

    tidy_df = pd.merge(
        tidy_df,
        df_evic_list[["year_mon", "geoid", "eviction_rate"]],
        left_on=["date", "tract"],
        right_on=["year_mon", "geoid"],
        how="left",
    )

    # Remove unnecessary columns
    tidy_df = tidy_df.drop(columns=["year_mon", "geoid"])

    # Fill census tracts with no evictions as eviction rate = 0
    tidy_df["eviction_rate"] = tidy_df["eviction_rate"].fillna(0)

    # Merge 311 call data
    encampment_reports_df = count_311_by_tract()
    encampment_reports_df = encampment_reports_df.rename(columns={"geoid": "tract"})

    tidy_df = pd.merge(tidy_df, encampment_reports_df, on=["date", "tract"], how="left")

    # Fill missing 311 calls with 0's
    tidy_df["311_calls"] = tidy_df["311_calls"].fillna(0)

    # Grab encampments data
    encampments_df = count_encampments_by_tract()
    encampments_df = encampments_df.rename(columns={"geoid": "tract"})

    # Interpolate encampments data to go from quarterly to monthly
    encampments_df["date"] = pd.to_datetime(encampments_df["date"])
    encampments_df = encampments_df.sort_values(["tract", "date"])

    interpolated_list = []

    for tract, tract_group in encampments_df.groupby("tract"):
        tract_group = tract_group.set_index("date", drop=False)

        # Add missing months to prepare for quarterly --> monthly interpolation
        all_months = pd.date_range(
            start=tract_group.index.min(), end=tract_group.index.max(), freq="MS"
        )
        tract_group = tract_group.reindex(all_months)

        tract_group["tract"] = tract

        # Convert to floats to prepare for interpolation
        encampment_cols = ["tents", "structures", "vehicles"]
        tract_group[encampment_cols] = tract_group[encampment_cols].astype(float)

        # Linear interpolation for all encampments (tents, structures, and vehicles)
        tract_group[encampment_cols] = tract_group[encampment_cols].interpolate(
            method="linear"
        )

        tract_group["date"] = tract_group.index
        tract_group = tract_group.reset_index(drop=True)

        interpolated_list.append(tract_group)

    encampments_df = pd.concat(interpolated_list, ignore_index=True)

    # Convert date back to string for proper merge
    encampments_df["date"] = encampments_df["date"].dt.strftime("%Y-%m")

    # Merge encampments data
    tidy_df = pd.merge(tidy_df, encampments_df, on=["date", "tract"], how="left")

    # Fill missing encampments with 0's
    tidy_df[["tents", "structures", "vehicles"]] = tidy_df[
        ["tents", "structures", "vehicles"]
    ].fillna(0)

    # Calculate weighted estimate of homelessness based on encampment types
    tidy_df["estimate"] = (
        tidy_df["tents"] * TENTS_EST
        + tidy_df["structures"] * STRUCTURES_EST
        + tidy_df["vehicles"] * VEHICLES_EST
    )

    # Sort dataframe for readability
    tidy_df = tidy_df.sort_values(["date", "tract"])

    tidy_df.to_csv(MERGED, index=False)
