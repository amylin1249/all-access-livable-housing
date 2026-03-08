import pandas as pd
import geopandas as gpd
import altair as alt
from pathlib import Path

from .datatypes import MERGED_SF_TRACTS_SHP, MERGED, CLEAN_ZILLOW

# from .datatypes import MERGED_SF_TRACTS_SHP, MERGED


def create_tract_map(start_date: str, end_date: str, col_name: str):
    """
    Create Altair choropleth map of SF tracts based on a specified metric
    averaged given a start date and end date.

    Parameters:
        start_date: Start date for analysis
        end_date: End date for analysis
        col_name: Column name for preferred metric of analysis

    Returns:
        An Altair choropleth map across SF tracts for the given metric and time
        period for analysis
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

    merged_df = pd.read_csv(MERGED)
    tracts_gdf = gpd.read_file(MERGED_SF_TRACTS_SHP)

    merged_df["tract"] = merged_df["tract"].astype(str).str.zfill(11)

    merged_df["date"] = pd.to_datetime(merged_df)
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)

    filtered_df = (
        merged_df[(merged_df["date"] >= start_dt) & (merged_df["date"] <= end_dt)]
        .drop(columns=["date"])
        .groupby("tract")
        .mean()
        .reset_index()
    )

    # Merge aggregated dataframe with GeoDataFrame
    merged_tracts_gdf = tracts_gdf.merge(filtered_df, left_on="GEOID", right_on="tract", how="left")

    # Create tooltips, and add last tooltip only if selected column name is not one of the existing tooltips
    tooltips = [
        alt.Tooltip("GEOID:N", title="Tract ID"),
        alt.Tooltip("population:Q", title="Population"),
        alt.Tooltip("median_rent:Q", format=",.0f", title="Median rent (per month)"),
        alt.Tooltip("eviction_rate:Q", format=".3%", title="Average eviction rate"),
        alt.Tooltip("estimate:Q", format=",.0f", title="Average homeless population estimate"),
        alt.Tooltip("311_calls:Q", format=",.0f", title="Average monthly citizen-reported encampments")
    ]

    if col_name in ["tents", "structures", "vehicles"]:
        tooltips.append(alt.Tooltip(f"{col_name}:Q", format=",.0f", title=f"Average {METRIC_NAMES[col_name].lower()}"))

    # Create base map for tracts with no data
    background = (
        alt.Chart(tracts_gdf)
        .mark_geoshape(fill="lightgray", stroke="white")
        .project("albersUsa")
    )

    # Build interactive choropleth map
    chart = (
        alt.Chart(merged_tracts_gdf)
        .mark_geoshape(stroke="black", strokeWidth=0.5)
        .encode(
            color=alt.Color(
                f"{col_name}:Q",
                title=METRIC_NAMES[col_name],
                legend=alt.Legend(
                    orient="right",
                    direction="vertical",
                    labelAlign="left",
                    titlePadding=5,
                    offset=10,
                ),
            ),
            tooltip=tooltips
        )
        .transform_lookup(
            lookup="GEOID",
            from_=alt.LookupData(filtered_df, "tract", ["metric"]),
        )
        .project(type="mercator", scale=120000, center=[-122.43, 37.77])
        .properties(width="container", height=550)
        .configure_view(stroke=None)
        .interactive()
    )

    return chart.resolve_scale(color="independent")


def create_reg_chart():

    variables = [
        ["Median Rent", "(Tract)"],
        ["Median Household", "Income (Tract)"],
        "Percentage White",
        "Total Tents",
        "Total Structures",
        "Total Vehicles",
    ]

    # Coefficients with varying effect sizes and significance
    coefficients = [-0.0005, -1.124e-05, 10.5250, 0.9523, 0.6413, -0.0452]
    std_errors = [0.001, 1.79e-05, 3.500, 0.127, 0.241, 0.027]

    # Calculate 95% confidence intervals
    ci_lower = [
        coefficients[i] - 1.96 * std_errors[i] for i in range(0, len(coefficients))
    ]
    ci_upper = [
        coefficients[i] + 1.96 * std_errors[i] for i in range(0, len(coefficients))
    ]

    # Determine significance
    significant = [
        (ci_lower[i] > 0 or ci_upper[i] < 0) for i in range(0, len(coefficients))
    ]

    df = pd.DataFrame(
        {
            "variable": variables,
            "coefficient": coefficients,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "significant": significant,
        }
    )

    # Error bars (confidence intervals)
    error_bars = (
        alt.Chart(df)
        .mark_rule(strokeWidth=3)
        .encode(
            x="ci_lower:Q",
            x2="ci_upper:Q",
            y=alt.Y("variable:N", sort=None),
            color=alt.condition(
                alt.datum.significant,
                alt.value("blue"),
                alt.value("black"),
            ),
        )
    )

    # Points (coefficient estimates)
    points = (
        alt.Chart(df)
        .mark_point(size=200, filled=True)
        .encode(
            x=alt.X("coefficient:Q", axis=alt.Axis(title="Coefficient Value")),
            y=alt.Y(
                "variable:N",
                sort="x",
                axis=alt.Axis(
                    title=None,
                    labelAlign="right",
                    labelFontSize=10,
                    labelAngle=-30,
                    labelPadding=10,
                ),
            ),
            color=alt.condition(
                alt.datum.significant,
                alt.value("blue"),
                alt.value("black"),
            ),
            tooltip=[
                alt.Tooltip("variable:N", title="Variable"),
                alt.Tooltip(
                    "coefficient:Q",
                    title="Coefficient (Unique 311 Reports)",
                    format=".3f",
                ),
                alt.Tooltip("significant:N", title="Significant"),
            ],
        )
    )

    x_zero = (
        alt.Chart(pd.DataFrame({"x": [0]}))
        .mark_rule(color="black", strokeDash=[4, 4])
        .encode(x="x:Q")
    )

    # Combine layers
    chart = (
        (x_zero + error_bars + points)
        .properties(
            width="container",
            height=450,
            padding={"left": 10, "right": 10, "top": 20, "bottom": 20},
            title=alt.Title(
                [
                    "Regression Analysis: Impact of Tract Features",
                    "on Total Number of Unique Reports",
                ],
                fontSize=15,
            ),
        )
        .configure_axis(labelFontSize=18, titleFontSize=22)
    )

    return chart.resolve_scale(color="independent")

<<<<<<< HEAD

def homeless_scatterplot(tract_id: str):
=======
def create_homeless_scatterplot(source_file: Path, tract_id: str):
>>>>>>> 9534b9259e1cbea67485c841f29192975d5978f5
    """
    Add docstring
    """

    df = pd.read_csv(MERGED)

    df["tract"] = df["tract"].astype(str).str.zfill(11)

    filtered_df = df[df["tract"] == tract_id]

    chart = (
        alt.Chart(filtered_df)
        .mark_line(point=True)
        .encode(x=alt.X("date:T"), y=alt.Y("estimate:Q"))
        .properties(title="temporary title")
    )

    return chart


<<<<<<< HEAD
def encampments_scatterplot(tract_id: str):
    df = pd.read_csv(MERGED)
=======
def create_encampments_scatterplot(source_file: Path, tract_id: str):
    df = pd.read_csv(source_file)
>>>>>>> 9534b9259e1cbea67485c841f29192975d5978f5

    df["tract"] = df["tract"].astype(str).str.zfill(11)

    filtered_df = df[df["tract"] == tract_id]

    folded_chart = (
            alt.Chart(filtered_df)
            .mark_line()
            .transform_fold(
                fold= ["Structures", "Tents", "Vehicles"],
                as_=["measurement", "value"],)
            .encode(
                x=alt.X("date:T"),
                y=alt.Y("value:Q"),
                color=alt.Color("measurement:N"),
        )
    )

    return folded_chart


def rent_scatterplot(zip_code: str):
    df = pd.read_csv(CLEAN_ZILLOW)

    df["zip"] = df["zip"].astype(str).str.zfill(5)

    filtered_df = df[df["zip"] == zip_code]

    chart = (
            alt.Chart(filtered_df)
            .mark_line()
            .encode(
                x=alt.X("date:T"),
                y=alt.Y("rent:Q"),
        )
    )

#     df = df.rename(
#             columns={
#                 "tents": "Tents",
#                 "vehicles": "Vehicles",
#                 "structures": "Structures",
#                 "tract": "Tract",
#                 "date": "Date",

#             }
#         )


#     tract_select = alt.selection_point(
#             fields=['Tract'],
#             bind=alt.binding_select(options=list(df['Tract'].unique()), name='Select Tract')
#         )


#     folded_chart = (
#             alt.Chart(df)
#             .mark_line()
#             .transform_fold(
#                 fold= ['Structures', 'Tents', 'Vehicles'],
#                 as_=["measurement", "value"],
#             ) .transform_filter(tract_select)
#             .encode(
#                 x=alt.X("Date", type="temporal", timeUnit="yearmonth"),
#                 y=alt.Y("value", type="quantitative"),
#                 color=alt.Color("measurement", type="nominal"),
#             ).add_params(tract_select)
#         )
#     folded_chart


if __name__ == "__main__":
    print(create_tract_map("2020-01", "2024-12", "estimate"))
    # create_scatterplot(
    #     MERGED,
    #     "estimate",
    #     "mean",
    #     "median_rent",
    #     "mean",
    # )
