import pandas as pd
import geopandas as gpd
import altair as alt
from .datatypes import MERGED_SF_TRACTS_SHP, MERGED, CLEAN_ZILLOW
from .regression_analysis import run_reg


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

    filtered_df = (
        merged_df[(merged_df["date"] >= start_date) & (merged_df["date"] <= end_date)]
        .drop(columns=["date"])
        .groupby("tract")
        .mean()
        .reset_index()
    )

    # Merge aggregated dataframe with GeoDataFrame
    merged_tracts_gdf = tracts_gdf.merge(
        filtered_df, left_on="GEOID", right_on="tract", how="left"
    )

    # Create tooltips, and add last tooltip only if selected column name is not one of the existing tooltips
    tooltips = [
        alt.Tooltip("GEOID:N", title="Tract ID"),
        alt.Tooltip("population:Q", title="Population"),
        alt.Tooltip("median_rent:Q", format=",.0f", title="Median rent (per month)"),
        alt.Tooltip("eviction_rate:Q", format=".3%", title="Average eviction rate"),
        alt.Tooltip(
            "estimate:Q", format=",.0f", title="Average homeless population estimate"
        ),
        alt.Tooltip(
            "311_calls:Q",
            format=",.0f",
            title="Average monthly citizen-reported encampments",
        ),
    ]

    if col_name in ["tents", "structures", "vehicles"]:
        tooltips.append(
            alt.Tooltip(
                f"{col_name}:Q",
                format=",.0f",
                title=f"Average {METRIC_NAMES[col_name].lower()}",
            )
        )

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
            tooltip=tooltips,
        )
        .transform_lookup(
            lookup="GEOID",
            from_=alt.LookupData(filtered_df, "tract", ["metric"]),
        )
        .project("albersUsa")
        .properties(width="container", height=550)
        # .configure_view(stroke=None)
        .interactive()
    )

    return background + chart


def create_reg_chart():
    """
    Create an Altair coefficient plot representing the results of a
    regression analysis on 311 service reports.
    The chart visualizes the point estimates and 95% confidence intervals
    for predictors such as rent, income, and physical encampment counts.

    Returns:
        An Altair chart object visualizing regression coefficients with  color encoding.
    """

    variables = [
        ["Median Rent", "(Tract)"],
        ["Median Household", "Income (Tract)"],
        "Percentage White",
        "Total Tents",
        "Total Structures",
        "Total Vehicles",
    ]

    # Coefficients with varying effect sizes and significance
    output = run_reg()
    coefficients = [
        output.params["med_rent"],
        output.params["med_hh_inc"],
        output.params["white_pct"],
        output.params["tents"],
        output.params["structures"],
        output.params["vehicles"],
    ]
    std_errors = [
        output.bse["med_rent"],
        output.bse["med_hh_inc"],
        output.bse["white_pct"],
        output.bse["tents"],
        output.bse["structures"],
        output.bse["vehicles"],
    ]

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


def create_rent_scatterplot(zip_code: str):
    """
    Create an Altair line chart showing the temporal trend of median monthly rent for a specific zip code using Zillow data.

    Parameters:
        zip_code (str): A 5-digit string representing the target zip code.

    Returns:
        An Altair line chart with a non-zero scaled Y-axis for better trend visibility.
    """
    df = pd.read_csv(CLEAN_ZILLOW)

    df["zip"] = df["zip"].astype(str).str.zfill(5)

    filtered_df = df[df["zip"] == zip_code]

    chart = (
        alt.Chart(filtered_df)
        .mark_line(point=True)
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y(
                "rent:Q", title="Median rent (per month)", scale=alt.Scale(zero=False)
            ),
        )
        .properties(
            width="container",
            height=450,
            autosize=alt.AutoSizeParams(type="fit", contains="padding"),
        )
    )

    return chart


def create_homeless_scatterplot(tract_id: str):
    """
    Create an Altair line chart showing the estimated homeless population trends over time for a specific census tract.

    Parameters:
        tract_id (str): An 11-digit string representing the target census tract.

    Returns:
        An Altair line chart visualizing temporal homeless population estimates.
    """

    df = pd.read_csv(MERGED)

    df["tract"] = df["tract"].astype(str).str.zfill(11)

    filtered_df = df[df["tract"] == tract_id]

    chart = (
        alt.Chart(filtered_df)
        .mark_line(point=True)
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("estimate:Q", title="Homeless Population Estimate"),
        )
        .properties(
            width="container",
            height=450,
            autosize=alt.AutoSizeParams(type="fit", contains="padding"),
        )
    )

    return chart


def create_encampments_scatterplot(tract_id: str):
    """
    Create a multi-series Altair line chart breaking down encampment types (tents, vehicles, and structures) over time for a specific tract.

    Parameters:
        tract_id (str): An 11-digit string representing the target census tract.

    Returns:
        An Altair chart object with folded data series for encampment breakdown.
    """
    df = pd.read_csv(MERGED)

    df["tract"] = df["tract"].astype(str).str.zfill(11)

    filtered_df = df[df["tract"] == tract_id]

    folded_chart = (
        alt.Chart(filtered_df)
        .mark_line(point=True)
        .transform_fold(
            fold=["structures", "tents", "vehicles"],
            as_=["measurement", "value"],
        )
        .encode(
            x=alt.X("date:T", axis=alt.Axis(format="%Y", tickCount=12, labelAngle=0)),
            y=alt.Y("value:Q"),
            color=alt.Color("measurement:N"),
        )
        .properties(width="container", height=350)
    )

    return folded_chart
