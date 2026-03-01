import pandas as pd
import csv
from pathlib import Path
from datetime import datetime

### COMBINE FIRST AND SECOND FUNCTIONS
def filter_zori():
    """
    Loads ZORI CSV file, filters for SF zip codes and the years 2020-2024 and 
    imputes to fill missing data.
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

    # Imputes data to fill missing values and outputs a CSV file.
    zip_col = filtered_df["zip"]
    data = filtered_df.drop(columns=["zip"])
    data = data.interpolate(axis=1)
    data = data.fillna(data.mean())
    imputed_df = pd.concat([zip_col, data], axis=1)
    imputed_df.to_csv("clean-data/imputed_zori.csv", index=False)


def reformat_zori_data():
    """
    Reformats Zori CSV into tidy format.
    """
    zips = set()
    with (
        open("clean-data/imputed_zori.csv") as f_in,
        open("clean-data/tidy_zori.csv", "w", newline="") as f_out,
    ):
        reader = csv.DictReader(f_in)
        writer = csv.DictWriter(f_out, fieldnames=["zip", "month", "rent"])
        month_cols = reader.fieldnames[1:]
        for row in reader:
            zip = row["zip"]
            zips.add(str(zip))
            for month in month_cols:
                writer.writerow({"zip": zip, "month": month, "rent": row[month]})
    return list(zips)


def reformat_crosswalks(zips):
    list_of_dfs = []
    for file_path in Path("raw-data/crosswalks-xlsx").iterdir():
        if not file_path.name.startswith("~$"):
            df = pd.read_excel(file_path, engine="openpyxl")
            zip_col = None
            for column in df.columns:
                if "zip" in column.lower():
                    zip_col = column
                    break
            df[zip_col] = df[zip_col].astype(str)
            sf_df = df[df[zip_col].isin(zips)]
            for column in df.columns:
                if "tract" in column.lower():
                    tract_col = column
                    break
            for column in df.columns:
                if "res_ratio" in column.lower():
                    res_ratio_col = column
                    break
            datetime_str = file_path.stem[-6:]
            datetime_object = datetime.strptime(datetime_str, "%m%Y")
            filtered_df = sf_df.loc[:, [zip_col, tract_col, res_ratio_col]]
            filtered_df["date"] = datetime_object
            filtered_df.rename(columns={"ZIP": "zip", "TRACT": "tract", "RES_RATIO": "res_ratio"}, inplace=True)
            list_of_dfs.append(filtered_df)
        aggregated_df = pd.concat(list_of_dfs, ignore_index=True)
        aggregated_df.to_csv('clean-data/crosswalks.csv', index=None, header=True)


# def weight_to_census_tract():
#     with open("clean-data/processed_zori.csv") as f:
#         reader = csv.DictReader(f)
#         for file_path in Path("clean-data/crosswalks-csv").iterdir():
#             df = pd.read_csv(file_path)
#             for row in reader:


if __name__ == "__main__":
    filter_zori()
    zips = reformat_zori_data()
    reformat_crosswalks(zips)
