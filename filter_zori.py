import pandas as pd


def get_cleaned_zori_dict():
    """
    load org zori file and filter sf data
    -return1 : sf_data_df(dataframe)
    -return2 : rent_dict {mon-year : [(zipcode, dollar amount)]}
    """
    # load data
    df = pd.read_csv("raw-data/zori_by_zip.csv")

    # column(City) ==  'San Francisco'
    zip_sf = df[df["City"] == "San Francisco"].copy()

    # filter month-year(2020-2024)
    date_cols = [
        col
        for col in zip_sf.columns
        if any(yr in col for yr in ["2020", "2021", "2022", "2023", "2024"])
    ]
    sf_data_df = zip_sf[["RegionName"] + date_cols]
    # change regionname to zip
    sf_data_df = sf_data_df.rename(columns={"RegionName": "zip"})

    sf_data_df.to_csv("zori_filter.csv", index=False)

    melted = sf_data_df.melt(id_vars="zip", var_name="date", value_name="rent")

    # change date format (MM-YYYY)
    melted["month_year"] = pd.to_datetime(melted["date"]).dt.strftime("%m-%Y")

    # make dic
    rent_dict = (
        melted.dropna(subset=["rent"])
        .groupby("month_year")
        .apply(lambda x: list(zip(x["zip"], x["rent"])))
        .to_dict()
    )

    return sf_data_df, rent_dict


if __name__ == "__main__":
    sf_table, sf_dict = get_cleaned_zori_dict()
