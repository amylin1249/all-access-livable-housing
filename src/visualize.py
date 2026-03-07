import pandas as pd
import geopandas as gpd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from datatypes import MERGED_SF_TRACTS_SHP, MERGED


def create_tract_map(
    source_file: Path, start_date: str, end_date: str, col_name: str
):
    """
    Add docstring
    """
    METRIC_NAMES = {
    "311_calls": "311 calls",
    "eviction_rate": "Eviction rate",
    "median_rent": "Median rent",
    "tents": "Tents",
    "structures": "Structures",
    "vehicles": "Vehicles",
    "estimate": "Homelessness estimate",
    }

    df = pd.read_csv(source_file)
    sf_tracts = gpd.read_file(MERGED_SF_TRACTS_SHP)
    ### TBD ON WHETHER THIS SHOULD BE INSIDE OR OUTSIDE FUNCTION

    df["tract"] = df["tract"].astype(str).str.zfill(11)

    filtered_df = (
        df[(df["date"] >= start_date) & (df["date"] <= end_date)]
        .groupby("tract")
        .agg(metric=(col_name, "mean"))
        .reset_index()
    )

    chart = (
        alt.Chart(sf_tracts)
        .mark_geoshape()
        .encode(
            color=alt.Color("metric:Q", title={METRIC_NAMES[col_name]}),
            tooltip=[
                alt.Tooltip("GEOID:N", title="Tract ID"),
                alt.Tooltip("population:Q", title="Population"),
                alt.Tooltip("med_hh_inc:Q", title="Median annual household income"),
                alt.Tooltip("white_pct:Q", title="% white population"),
                alt.Tooltip("metric:Q", title=f"Monthly average {METRIC_NAMES[col_name].lower()}"),
            ],
        )
        .transform_lookup(
            lookup="GEOID",
            from_=alt.LookupData(filtered_df, ("tract"), ["metric"]),
        )
        .project(type="albersUsa")
        .properties(
            title=f"Average {METRIC_NAMES[col_name].lower()} in SF tracts ({start_date} to {end_date})"
        )
        .interactive()
    )

    return chart


def create_scatterplot(
    source_file: Path, x_var: str, x_agg: str, y_var: str, y_agg: str
):
    """
    Docstring
    """
    sns.set_theme(style="whitegrid")

    # Load dataset
    df = pd.read_csv(source_file)
    filtered_df = (
        df.groupby("tract")
        .agg(x_axis=(x_var, x_agg), y_axis=(y_var, y_agg))
        .reset_index()
    )

    # Draw a scatter plot while assigning point colors and sizes to different
    # variables in the dataset
    f, ax = plt.subplots(figsize=(6.5, 6.5))
    sns.despine(f, left=True, bottom=True)
    sns.scatterplot(
        x="x_axis",
        y="y_axis",
        # hue="white_pct",
        # size="population",  ### To update these to the right metrics once dataset finalized
        palette="ch:r=-.2,d=.3_r",
        sizes=(1, 100),
        linewidth=0,
        data=filtered_df,
        ax=ax,
    )
    plt.xlabel("Average homelessness counts", fontsize=12)
    plt.ylabel("Median monthly rent ($)", fontsize=12)
    plt.title(
        "Median rent by tract vs. Average homelessness counts",
        fontsize=14,
        fontweight="bold",
    )
    plt.show()


if __name__ == "__main__":
    create_tract_map(MERGED, "2020-01", "2024-12", "estimate")
    # create_scatterplot(
    #     MERGED,
    #     "estimate",
    #     "mean",
    #     "median_rent",
    #     "mean",
    # )
