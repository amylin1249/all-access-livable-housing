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


def generate_crosswalks_csv(zips):
    """
    Loads crosswalks XLSX files, filters for SF, selects necessary columns (zip, 
    tract, res_ratio), extracts date column from filenames, and outputs into single
    CSV.

    Inputs:
        zips: [list] SF zip codes
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
    