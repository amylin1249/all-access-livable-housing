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
        writer = csv.DictWriter(f_out, fieldnames=["zip", "date", "rent"])
        writer.writeheader()
        month_cols = reader.fieldnames[1:]
        for row in reader:
            zip = row["zip"]
            zips.add(str(zip))
            for month in month_cols:
                datetime_object = datetime.strptime(month, "%Y-%m-%d")
                date = str(datetime_object.year) + "-" + str(datetime_object.month)
                writer.writerow({"zip": zip, "date": date, "rent": row[month]})
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
            date = str(datetime_object.year) + "-" + str(datetime_object.month)
            filtered_df = sf_df.loc[:, [zip_col, tract_col, res_ratio_col]]
            filtered_df["date"] = date
            filtered_df.rename(columns={"ZIP": "zip", "TRACT": "tract", "RES_RATIO": "res_ratio"}, inplace=True)
            list_of_dfs.append(filtered_df)
        aggregated_df = pd.concat(list_of_dfs)
        aggregated_df.to_csv('clean-data/crosswalks.csv', index=None, header=True)


def generate_crosswalks_dict():
    crosswalks_dict = {}
    with open("clean-data/crosswalks.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["date"] not in crosswalks_dict:
                crosswalks_dict[row["date"]] = {}
            if row["zip"] not in crosswalks_dict[row["date"]]:
                crosswalks_dict[row["date"]][row["zip"]] = []
            crosswalks_dict[row["date"]][row["zip"]].append((row["tract"], row["res_ratio"]))
    
    for year in range(2020,2025):
        for month in range(1,13):
            current_date = str(year) + "-" + str(month)
            if current_date not in crosswalks_dict:
                if month <= 3:
                    crosswalks_dict[current_date] = crosswalks_dict[str(year) + "-" + str(3)]
                elif month <= 6:
                    crosswalks_dict[current_date] = crosswalks_dict[str(year) + "-" + str(6)]
                elif month <= 9:
                    crosswalks_dict[current_date] = crosswalks_dict[str(year) + "-" + str(9)]
                else:
                    crosswalks_dict[current_date] = crosswalks_dict[str(year) + "-" + str(12)]
    return crosswalks_dict


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


def weight_to_census_tract(crosswalks_dict, rent_by_zip):
    weighted_dict = {}
    for date in crosswalks_dict:
        for zip in crosswalks_dict[date]:
            for tract, weight in crosswalks_dict[date][zip]:
                if date not in weighted_dict:
                    weighted_dict[date] = {}
                if tract not in weighted_dict[date]:
                    weighted_dict[date][tract] = 0
                weighted_dict[date][tract] += float(rent_by_zip[date][zip]) * float(weight)
    return weighted_dict


if __name__ == "__main__":
    # filter_zori()
    # zips = reformat_zori_data()
    # reformat_crosswalks(zips)
    crosswalks_dict = generate_crosswalks_dict()
    rent_by_zip = generate_rent_by_zip_dict()
    weighted_dict = weight_to_census_tract(crosswalks_dict, rent_by_zip)
    print(len(sorted(weighted_dict.keys())))