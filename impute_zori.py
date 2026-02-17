import pandas as pd


def impute_zori_data(path):
    """
    Fill in missing data in ZORI file
    """
    df = pd.read_csv(path)
    zip_col = df["zip"]
    data = df.drop(columns=["zip"])
    data = data.interpolate(axis=1)
    data = data.fillna(data.mean())
    df_clean = pd.concat([zip_col, data], axis=1)
    df_clean.to_csv("clean-data/imputed_zori.csv", index=False)


# CSV version
#     with open(path, "r", newline="") as infile, open('clean-data/imputed_zori.csv', "w", newline="") as outfile:
#         reader = csv.DictReader(infile, delimiter=",")
#         writer = csv.DictWriter(outfile, fieldnames=fieldnames)
#         for row in reader:
#             if is_row_empty(row):
#                 writer.writerow()

# def is_row_empty(row):
#     for entry in row.values():
#         if entry != "":
#             return False
#     return True

# def is_row_filled(row):
#     for entry in row.values():
#         if entry == "":
#             return False
#     return True

if __name__ == "__main__":
    impute_zori_data("clean-data/zori_filter.csv")
