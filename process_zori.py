import pandas as pd


def filter_zori():
    """
    Loads ZORI CSV file and filters for SF zip codes and the years 2020-2024. 

    Returns: sf_data_df (Pandas dataframe)
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
    sf_data_df = sf_zips[["RegionName"] + date_cols]
    # change regionname to zip
    sf_data_df = sf_data_df.rename(columns={"RegionName": "zip"})

    return sf_data_df

def impute_zori_data(df):
    """
    Imputes data to fill missing values and outputs a CSV file with the final data.

    Inputs: df (Pandas dataframe)
    """
    zip_col = df["zip"]
    data = df.drop(columns=["zip"])
    data = data.interpolate(axis=1)
    data = data.fillna(data.mean())
    df_clean = pd.concat([zip_col, data], axis=1)
    df_clean.to_csv("clean-data/processed_zori.csv", index=False)

if __name__ == "__main__":
    sf_df = filter_zori()
    impute_zori_data(sf_df)
