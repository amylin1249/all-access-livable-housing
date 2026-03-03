import pandas as pd
import csv
from pathlib import Path
from datetime import datetime


def generate_zori_csv():
    """
    Loads ZORI CSV file, filters for SF zip codes and the years 2020-2024, imputes 
    to fill missing data, and outputs tidy ZORI CSV.
    
    Returns:
        zips: [list] SF zip codes
        rent_by_zip: [dict] monthly rent per zip code in SF
    """
    # load data
    df = pd.read_csv("raw-data/zori_by_zip.csv")

    # column(City) ==  'San Francisco'
    sf_zips = df[df["City"] == "San Francisco"].copy()

    # filter month-year(2020-2024)
    date_cols = [
        col
        for col in sf_zips.columns
        if any(yr in col for yr in ["2020", "2021", "2022", "2023", "2024"])
    ]

    filtered_df = sf_zips[["RegionName"] + date_cols]
    # change regionname to zip
    filtered_df = filtered_df.rename(columns={"RegionName": "zip"})

    # Imputes data to fill missing values
    zip_col = filtered_df["zip"]
    data = filtered_df.drop(columns=["zip"])
    data = data.interpolate(axis=1)
    data = data.fillna(data.mean())
    imputed_df = pd.concat([zip_col, data], axis=1)

    # Reformats Zori CSV into tidy format
    zips = set()
    tidy_rows = []
    date_cols = imputed_df.drop(columns=["zip"]).columns
    for _, row in imputed_df.iterrows():
        # Avoid conversion to float by converting to string
        zip_code = str(int(row["zip"]))
        zips.add(zip_code)
        for date in date_cols:
            datetime_object = datetime.strptime(date, "%Y-%m-%d")
            formatted_date = f"{datetime_object.year}-{datetime_object.month:02}"
            tidy_rows.append({"zip": zip_code, "date": formatted_date, "rent": row[date]})

    # Writes tidy CSV
    with open("clean-data/tidy_zori.csv", "w", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=["zip", "date", "rent"])
        writer.writeheader()
        writer.writerows(tidy_rows)

    # Build rent_by_zip dictionary
    rent_by_zip = {}
    for row in tidy_rows:
        if row["date"] not in rent_by_zip:
            rent_by_zip[row["date"]] = {}
        if row["zip"] not in rent_by_zip[row["date"]]:
            rent_by_zip[row["date"]][row["zip"]] = row["rent"]

    return list(zips), rent_by_zip


def generate_crosswalks_csv(zips):
    """
    Loads crosswalks XLSX files, filters for SF, selects necessary columns (zip, 
    tract, res_ratio), extracts date column from filenames, and outputs into single
    CSV.

    Inputs:
        zips: [list] SF zip codes
    Returns:
        crosswalks: [dict] monthly crosswalk data per SF zip code, with 
        (tract, res_ratio)
    """
    list_of_dfs = []
    for file_path in Path("raw-data/crosswalks-xlsx").iterdir():
        if not file_path.name.startswith("~$"):
            df = pd.read_excel(file_path, engine="openpyxl")
            zip_col = None
            # Pull zip, tract, and res_ratio columns for SF zips
            for column in df.columns:
                if "zip" in column.lower():
                    zip_col = column
                    break
            df[zip_col] = df[zip_col].astype(str)
            sf_df = df[df[zip_col].isin(zips)]
            ### ADD FILTER FOR SF TRACTS BASED ON CENSUS_ACS_JOIN.CSV?
            for column in df.columns:
                if "tract" in column.lower():
                    tract_col = column
                    break
            for column in df.columns:
                if "res_ratio" in column.lower():
                    res_ratio_col = column
                    break
            # Add date column based on filename
            datetime_str = file_path.stem[-6:]
            datetime_object = datetime.strptime(datetime_str, "%m%Y")
            date = f"{datetime_object.year}-{datetime_object.month:02}"
            filtered_df = sf_df.loc[:, [zip_col, tract_col, res_ratio_col]]
            filtered_df["date"] = date
            filtered_df.rename(
                columns={"ZIP": "zip", "TRACT": "tract", "RES_RATIO": "res_ratio"}, inplace=True
            )
            list_of_dfs.append(filtered_df)
    
    # Aggregate and output to CSV
    aggregated_df = pd.concat(list_of_dfs)
    aggregated_df.to_csv("clean-data/crosswalks.csv", index=None, header=True)
    
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


if __name__ == "__main__":
    zips, rent_by_zip = generate_zori_csv()
    crosswalks = generate_crosswalks_csv(zips)
    rent_by_tract = weight_to_census_tract(crosswalks, rent_by_zip)
    