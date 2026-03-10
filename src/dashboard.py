import calendar
import pandas as pd
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from dash import Dash, html, dcc, Input, Output, exceptions
from .datatypes import MERGED, CLEAN_ZILLOW
from .visualize import (
    create_tract_map,
    create_reg_chart,
    create_rent_scatterplot,
    create_homeless_scatterplot,
    create_encampments_scatterplot,
)


df_merged = pd.read_csv(MERGED)
all_tracts = sorted(df_merged["tract"].astype(str).str.zfill(11).unique())

try:
    df_zillow = pd.read_csv(CLEAN_ZILLOW)
    all_zips = sorted(df_zillow["zip"].astype(str).str.zfill(5).unique())
except Exception:
    all_zips = []


app = Dash(
    __name__, external_stylesheets=[dbc.themes.MORPH], suppress_callback_exceptions=True
)

app.layout = html.Div(
    [
        # [Title]
        html.H1(
            "San Francisco Housing & Homelessness Dashboard",
            className="mt-4",
            style={"textAlign": "center", "color": "#2c3e50"},
        ),
        html.Br(),
        # [Description]
        html.Div(
            [
                html.Hr(),
                html.P(
                    "San Francisco has experienced significant changes in housing and homelessness over the past several years. "
                    "Many factors, including rising rents and increased evictions, have contributed to a growing number of unhoused individuals across the city. "
                    "This interactive dashboard combines multiple data sources to provide a clearer picture of these trends. "
                    "Eviction rates and median monthly rent estimates help illustrate the pressures on housing affordability, "
                    "while citizen-reported encampments (311 service calls), city-reported encampments (official counts), and street homeless population estimates "
                    "provide insights into patterns and concentrations of unhoused residents across the city. "
                    "Use the features below to explore how these metrics vary across San Francisco's census tracts over time."
                ),
                html.Hr(),
            ],
            style={"padding": "10px 40px", "color": "#34495e"},
        ),
        # [basic number showing]
        html.Div(
            [
                html.Div(
                    [
                        html.B("Street Homeless Population Estimate"),
                        html.Br(),
                        f"2021 (average): {df_merged[df_merged['date'].between('2021-01', '2021-12')]['estimate'].mean():,.0f}",
                        html.Br(),
                        f"2024 (average): {df_merged[df_merged['date'].between('2024-01', '2024-12')]['estimate'].mean():,.0f}",
                        html.Br(),
                        f"Annual % change: {((df_merged[df_merged['date'].between('2024-01', '2024-12')]['estimate'].mean() / df_merged[df_merged['date'].between('2021-01', '2021-12')]['estimate'].mean()) ** (1 / 3) - 1):.2%}",
                    ],
                    style={"flex": "1", "textAlign": "center"},
                ),
                html.Div("|", style={"fontSize": "24px", "color": "#ddd"}),
                html.Div(
                    [
                        html.B("Median Monthly Rent"),
                        html.Br(),
                        f"2021 (average): ${df_merged[df_merged['date'].between('2021-01', '2021-12')]['median_rent'].mean():,.0f}",
                        html.Br(),
                        f"2024 (average): ${df_merged[df_merged['date'].between('2024-01', '2024-12')]['median_rent'].mean():,.0f}",
                        html.Br(),
                        f"Annual % change: {((df_merged[df_merged['date'].between('2024-01', '2024-12')]['median_rent'].mean() / df_merged[df_merged['date'].between('2021-01', '2021-12')]['median_rent'].mean()) ** (1 / 3) - 1):.2%}",
                    ],
                    style={"flex": "1", "textAlign": "center"},
                ),
                html.Div("|", style={"fontSize": "24px", "color": "#ddd"}),
                html.Div(
                    [
                        html.B("311 Calls for Encampments"),
                        html.Br(),
                        f"2021 (average): {df_merged[df_merged['date'].between('2021-01', '2021-12')]['311_calls'].mean():,.0f}",
                        html.Br(),
                        f"2024 (average): {df_merged[df_merged['date'].between('2024-01', '2024-12')]['311_calls'].mean():,.0f}",
                        html.Br(),
                        f"Annual % change: {((df_merged[df_merged['date'].between('2024-01', '2024-12')]['311_calls'].mean() / df_merged[df_merged['date'].between('2021-01', '2021-12')]['311_calls'].mean()) ** (1 / 3) - 1):.2%}",
                    ],
                    style={"flex": "1", "textAlign": "center"},
                ),
            ],
            style={
                "display": "flex",
                "alignItems": "center",
                "padding": "20px",
                "margin": "20px 40px",
                "backgroundColor": "white",
                "borderRadius": "10px",
                "border": "1px solid #eee",
            },
        ),
        # [Tabs]
        dcc.Tabs(
            id="tabs-content",
            value="tab-map",
            children=[
                dcc.Tab(label="Geospatial Map", value="tab-map"),
                dcc.Tab(
                    label="Street Homeless Population Estimate", value="tab-homeless"
                ),
                dcc.Tab(label="Median Monthly Rent", value="tab-rent"),
                dcc.Tab(label="Regression Analysis of 311 Calls", value="tab-reg"),
            ],
            style={"margin": "20px 40px"},
        ),
        # [Content Container]
        html.Div(id="tabs-content-container", style={"padding": "0 40px"}),
    ],
    style={"maxWidth": "1600px", "margin": "0 auto", "boxSizing": "border-box"},
)


@app.callback(
    Output("tabs-content-container", "children"), Input("tabs-content", "value")
)
def render_content(tab):
    # [tab 1. map]
    if tab == "tab-map":
        return html.Div(
            [
                # first box : title and texts
                html.Div(
                    [
                        html.Div(
                            [
                                html.B(
                                    "Which parts of San Francisco have a higher concentration of street homeless individuals?"
                                ),
                                html.Br(),
                                html.B(
                                    "Where are median rents higher, and where are people being evicted?"
                                ),
                            ],
                            style={
                                "fontSize": "20px",
                                "lineHeight": "1",
                                "marginBottom": "20px",
                                "textAlign": "center",
                            },
                        ),
                        html.Div(
                            [
                                "These questions can be answered using the ",
                                html.B("interactive map"),
                                " below.",
                            ],
                            style={
                                "fontSize": "16px",
                                "lineHeight": "1.5",
                                "marginBottom": "20px",
                            },
                        ),
                        html.Div(
                            [
                                html.B("How to use: "),
                                "Select your ",
                                html.B("metric of interest"),
                                " and ",
                                html.B("start and end dates"),
                                " from the ",
                                html.B("dropdown menu"),
                                " below. The map will automatically update based on your selection.",
                            ],
                            style={
                                "fontSize": "16px",
                                "lineHeight": "1.5",
                                "marginBottom": "20px",
                            },
                        ),
                        # Metric Dropdown
                        html.Label("Select Metric:"),
                        dcc.Dropdown(
                            id="column-dropdown",
                            options=[
                                {
                                    "label": "Street Homeless Population Estimate",
                                    "value": "estimate",
                                },
                                {
                                    "label": "Median Monthly Rent",
                                    "value": "median_rent",
                                },
                                {"label": "Eviction Rate", "value": "eviction_rate"},
                                {
                                    "label": "Citizen-Reported Encampments (311 Calls)",
                                    "value": "311_calls",
                                },
                                {"label": "Official City Tent Count", "value": "tents"},
                                {
                                    "label": "Official City Structure Count",
                                    "value": "structures",
                                },
                                {
                                    "label": "Official City Lived-in Vehicle Count",
                                    "value": "vehicles",
                                },
                            ],
                            value="estimate",
                        ),
                        html.Br(),
                        # Date Selectors
                        html.Div(
                            [
                                # Start Period
                                html.Div(
                                    [
                                        html.Label("Start Period:"),
                                        dcc.Dropdown(
                                            id="start-month",
                                            options=[
                                                {
                                                    "label": calendar.month_name[m],
                                                    "value": f"{m:02d}",
                                                }
                                                for m in range(1, 13)
                                            ],
                                            value="01",
                                            style={
                                                "width": "150px",
                                                "display": "inline-block",
                                                "marginLeft": "10px",
                                            },
                                        ),
                                        dcc.Dropdown(
                                            id="start-year",
                                            options=[
                                                {"label": str(y), "value": str(y)}
                                                for y in range(2020, 2025)
                                            ],
                                            value="2020",
                                            style={
                                                "width": "120px",
                                                "display": "inline-block",
                                            },
                                        ),
                                    ],
                                    style={"display": "inline-block"},
                                ),
                                # End Period
                                html.Div(
                                    [
                                        html.Label(
                                            "End Period:", style={"marginLeft": "30px"}
                                        ),
                                        dcc.Dropdown(
                                            id="end-month",
                                            options=[
                                                {
                                                    "label": calendar.month_name[m],
                                                    "value": f"{m:02d}",
                                                }
                                                for m in range(1, 13)
                                            ],
                                            value="12",
                                            style={
                                                "width": "150px",
                                                "display": "inline-block",
                                                "marginLeft": "10px",
                                            },
                                        ),
                                        dcc.Dropdown(
                                            id="end-year",
                                            options=[
                                                {"label": str(y), "value": str(y)}
                                                for y in range(2020, 2025)
                                            ],
                                            value="2024",
                                            style={
                                                "width": "120px",
                                                "display": "inline-block",
                                                "marginLeft": "10px",
                                            },
                                        ),
                                    ],
                                    style={"display": "inline-block"},
                                ),
                            ]
                        ),
                    ],
                    style={
                        "padding": "20px",
                        "backgroundColor": "white",
                        "borderRadius": "10px",
                        "marginBottom": "20px",
                    },
                ),
                # second box : map
                html.Div(
                    [
                        html.H3(
                            id="map-title",
                            style={
                                "textAlign": "center",
                                "color": "#2c3e50",
                                "marginBottom": "15px",
                            },
                        ),
                        html.Hr(),
                        dvc.Vega(
                            id="sf-map",
                            spec={},
                            style={
                                "width": "100%",
                                "height": "600px",
                                "borderRadius": "10px",
                                "margin": "0 auto",
                            },
                        ),
                    ],
                    style={
                        "padding": "20px",
                        "border": "1px solid #ddd",
                        "borderRadius": "10px",
                        "backgroundColor": "white",
                    },
                ),
            ]
        )

    # [tab2. homeless]
    if tab == "tab-homeless":
        return html.Div(
            [
                # first box : itle and texts
                html.Div(
                    [
                        # texts
                        html.Div(
                            [
                                html.B(
                                    "How has the street homeless population in my neighborhood changed over time?"
                                ),
                                html.Br(),
                                html.B(
                                    "What is the distribution of tents, structures, and lived-in vehicles?"
                                ),
                            ],
                            style={
                                "fontSize": "20px",
                                "lineHeight": "1",
                                "marginBottom": "20px",
                                "textAlign": "center",
                            },
                        ),
                        html.Div(
                            [
                                "These questions can be answered using the ",
                                html.B("interactive scatterplots"),
                                " below, which track the ",
                                html.B("street homeless population estimate"),
                                " and ",
                                html.B("city-reported encampments (official counts)"),
                                " over ",
                                html.B("time"),
                                ". While the graph on the right shows the distribution of encampment types (tents, structures, and lived-in vehicles), the graph on the left shows street homeless population estimates, calculated by multiplying each encampment count by the average number of people residing in a tent, structure, or lived-in vehicle. The ",
                                html.B(
                                    "highest average street homeless population estimates"
                                ),
                                " from 2020 to 2024 are ",
                                html.B("6075980900 (Islais Creek)"),
                                ", ",
                                html.B("6075017700 (SoMa/the Mission)"),
                                ", and ",
                                html.B("6075023200 (Bayview-Hunters Point)"),
                                ". Street homelessness in Islais Creek and Bayview–Hunters Point is largely driven by individuals living in vehicles, while SoMa/the Mission is historically known for visible encampments, like tents and structures.",
                            ],
                            style={
                                "fontSize": "16px",
                                "lineHeight": "1.5",
                                "marginBottom": "20px",
                            },
                        ),
                        html.Div(
                            [
                                html.B("How to use: "),
                                "Select your ",
                                html.B("census tract ID"),
                                " from the ",
                                html.B("dropdown menu"),
                                " below. The graph will automatically update based on your selection.",
                            ],
                            style={
                                "fontSize": "16px",
                                "lineHeight": "1.5",
                                "marginBottom": "20px",
                            },
                        ),
                        # dropdown
                        html.Label("Select Census Tract ID:"),
                        dcc.Dropdown(
                            id="tract-dropdown",
                            options=[
                                {"label": str(t), "value": str(t)} for t in all_tracts
                            ],
                            value="06075017700",
                            clearable=False,
                            style={"width": "300px", "color": "black"},
                        ),
                    ],
                    style={
                        "padding": "20px",
                        "backgroundColor": "white",
                        "borderRadius": "10px",
                        "marginBottom": "30px",
                        "border": "1px solid #e9ecef",
                    },
                ),
                # second box : scatter plots
                html.Div(
                    [
                        # left plot
                        html.Div(
                            [
                                html.H4(
                                    id="homeless-title-1", style={"textAlign": "center"}
                                ),
                                dvc.Vega(
                                    id="homeless-1",
                                    spec={},
                                    style={"width": "100%", "height": "400px"},
                                ),
                            ],
                            style={
                                "width": "48%",
                                "padding": "10px",
                                "border": "1px solid #eee",
                                "borderRadius": "10px",
                                "backgroundColor": "white",
                            },
                        ),
                        # right plot
                        html.Div(
                            [
                                html.H4(
                                    id="homeless-title-2", style={"textAlign": "center"}
                                ),
                                dvc.Vega(
                                    id="homeless-2",
                                    spec={},
                                    style={"width": "100%", "height": "400px"},
                                ),
                            ],
                            style={
                                "width": "48%",
                                "padding": "10px",
                                "border": "1px solid #eee",
                                "borderRadius": "10px",
                                "marginLeft": "4%",
                                "backgroundColor": "white",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "flexDirection": "row",
                        "justifyContent": "space-between",
                        "alignItems": "stretch",
                    },
                ),
            ]
        )

    # [tab 3. Rent Scatter Plot]
    elif tab == "tab-rent":
        return html.Div(
            [
                # first box : title and texts
                html.Div(
                    [
                        html.Div(
                            [
                                html.B(
                                    "How has the monthly rent in my neighborhood changed over time?"
                                ),
                                html.Br(),
                                html.B(
                                    "What was the impact of the COVID-19 pandemic on rents?"
                                ),
                            ],
                            style={
                                "fontSize": "20px",
                                "lineHeight": "1",
                                "marginBottom": "20px",
                                "textAlign": "center",
                            },
                        ),
                        html.Div(
                            [
                                "These questions can be answered using the ",
                                html.B("interactive scatterplot"),
                                " below, which tracks ",
                                html.B("median monthly rent"),
                                " over ",
                                html.B("time"),
                                ". The three ZIP codes with the ",
                                html.B("highest average median monthly rent"),
                                " from 2020 to 2024 are ",
                                html.B("94158 (Mission Bay)"),
                                ", ",
                                html.B("94105 (Financial District/South Beach)"),
                                ", and ",
                                html.B("94114 (the Castro/Noe Valley)"),
                                ". Mission Bay and the Financial District/South Beach have a high concentration of luxury rental apartments and are located near major tech and finance employment centers, while Noe Valley is a historic and highly desirable residential neighborhood with limited housing supply.",
                            ],
                            style={
                                "fontSize": "16px",
                                "lineHeight": "1.5",
                                "marginBottom": "20px",
                            },
                        ),
                        html.Div(
                            [
                                html.B("How to use: "),
                                "Select your ",
                                html.B("zip code"),
                                " from the ",
                                html.B("dropdown menu"),
                                " below. The graph will automatically update based on your selection.",
                            ],
                            style={
                                "fontSize": "16px",
                                "lineHeight": "1.5",
                                "marginBottom": "20px",
                            },
                        ),
                        # dropdown
                        html.Label("Select Zip Code:"),
                        dcc.Dropdown(
                            id="zip-dropdown",
                            options=[
                                {"label": str(z), "value": str(z)} for z in all_zips
                            ],
                            value="94158",
                            clearable=False,
                        ),
                    ],
                    style={
                        "padding": "20px",
                        "backgroundColor": "white",
                        "borderRadius": "10px",
                        "marginBottom": "20px",
                    },
                ),
                # second box : scatter plot
                html.Div(
                    [
                        html.H3(id="rent-plot-title", style={"textAlign": "center"}),
                        html.Hr(),
                        dvc.Vega(
                            id="rent-scatter-plot",
                            spec={},
                            style={"width": "100%", "height": "500px"},
                        ),
                    ],
                    style={
                        "padding": "20px",
                        "border": "1px solid #ddd",
                        "borderRadius": "10px",
                        "backgroundColor": "white",
                    },
                ),
            ]
        )

    # [tab 4. reg]
    else:
        return html.Div(
            [
                # first box : title
                html.Div(
                    [
                        html.Div(
                            [
                                html.B(
                                    "How does the number of citizen-reported encampments (311 calls) correlate with tract-level characteristics?"
                                ),
                            ],
                            style={
                                "fontSize": "20px",
                                "lineHeight": "1",
                                "marginBottom": "20px",
                                "textAlign": "center",
                            },
                        ),
                    ],
                    style={
                        "padding": "30px",
                        "backgroundColor": "#f9f9f9",
                        "borderRadius": "10px",
                        "marginBottom": "20px",
                        "border": "1px solid #ddd",
                    },
                ),
                # second box : texts and regression
                html.Div(
                    [
                        html.Div(
                            [
                                # explaination
                                html.P(
                                    "We ran a regression to examine how tract-level characteristics are associated with the number of encampments reported through 311 service calls (e.g., the number of encampments that citizens reported to the City of San Francisco by calling the 311 service number). For each month with official city encampment counts, we matched those counts to the total number of 311 calls for encampments for that month, along with tract-level demographic and socioeconomic characteristics from the ACS.",
                                    style={"marginBottom": "15px"},
                                ),
                                html.P(
                                    "The regression included month fixed effects. The results indicate that median household income and median monthly rent are not significantly associated with the number of citizen reports via 311 calls. However, a tract's racial composition appears to be related to reporting behavior among residents: for every 10-percentage-point increase in the share of tract residents who are white, approximately 1 additional encampment location is reported per month. Note that we de-duplicated the data, such that calls for the same address or latitude and longitude were only counted once.",
                                    style={"marginBottom": "15px"},
                                ),
                                html.P(
                                    "Certain encampment characteristics are also strongly associated with reporting. For every 0.94 additional tents observed in the official city count, approximately 1 additional encampment location is reported per month. And for every 0.64 additional structures observed in the official city count, approximately 1 additional encampment location is reported per month. In contrast, the number of lived-in vehicles in the official city count has no clear relationship with the number of 311 calls. One possible explanation is that lived-in vehicles blend more easily into the surrounding environment, and therefore, citizens may not perceive them as a homeless encampment."
                                ),
                                # regression
                                dvc.Vega(
                                    id="reg-chart",
                                    spec={},
                                    style={"width": "100%", "height": "500px"},
                                ),
                            ],
                            style={
                                "padding": "25px",
                                "border": "1px solid #eee",
                                "borderRadius": "10px",
                                "backgroundColor": "#fff",
                                "lineHeight": "1.6",
                            },
                        )
                    ],
                    style={
                        "padding": "25px",
                        "border": "1px solid #ddd",
                        "borderRadius": "10px",
                        "backgroundColor": "white",
                        "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
                    },
                ),
            ]
        )


# tab1 : map
@app.callback(
    [
        Output("sf-map", "spec"),  # update
        Output("map-title", "children"),  # title-map
    ],
    [
        Input("column-dropdown", "value"),  # change in column
        Input("start-year", "value"),  # change in start-date
        Input("start-month", "value"),
        Input("end-year", "value"),  # change in end-date
        Input("end-month", "value"),
    ],
)
def update_map(selected_col, start_year, start_month, end_year, end_month):
    if any(
        v is None for v in [selected_col, start_year, start_month, end_year, end_month]
    ):
        raise exceptions.PreventUpdate

    METRIC_NAMES = {
        "311_calls": "Citizen-reported encampments (311 calls)",
        "eviction_rate": "Eviction rate",
        "median_rent": "Median monthly rent",
        "tents": "Official city tent count",
        "structures": "Official city structure count",
        "vehicles": "Official city lived-in vehicle count",
        "estimate": "Street homeless population estimate",
    }

    MONTHS = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December",
    }

    start_dt = f"{start_year}-{start_month}-01"
    year_num = int(end_year)
    month_num = int(end_month)
    last_day = calendar.monthrange(year_num, month_num)[1]
    end_dt = f"{end_year}-{end_month}-{last_day}"

    map_chart = create_tract_map(
        start_date=start_dt,
        end_date=end_dt,
        col_name=selected_col,
        # agg="mean",
    )

    map_title = f"{METRIC_NAMES[selected_col]}, averaged over {MONTHS[start_month]} {start_year} to {MONTHS[end_month]} {end_year}"

    return map_chart.to_dict(), map_title


# tab 2 : homeless scatterplot
@app.callback(
    [
        Output("homeless-1", "spec"),  # update
        Output("homeless-title-1", "children"),
        Output("homeless-2", "spec"),
        Output("homeless-title-2", "children"),
    ],
    [Input("tabs-content", "value"), Input("tract-dropdown", "value")],
)
def update_homeless_scatter(tab_value, selected_tract):
    if tab_value != "tab-homeless" or not selected_tract:
        raise exceptions.PreventUpdate

    homeless_scatterplot = create_homeless_scatterplot(tract_id=selected_tract)
    homeless_title1 = f"Street homeless population estimate over time in census tract {selected_tract}"

    encampments_scatterplot = create_encampments_scatterplot(tract_id=selected_tract)
    encampment_title = f"City-reported encampments (official counts) over time in census tract {selected_tract}"

    return (
        homeless_scatterplot.to_dict(),
        homeless_title1,
        encampments_scatterplot.to_dict(),
        encampment_title,
    )


# tab3 : rent scatterplot
@app.callback(
    [
        Output("rent-scatter-plot", "spec"),
        Output("rent-plot-title", "children"),
    ],  # update
    [Input("tabs-content", "value"), Input("zip-dropdown", "value")],
)
def update_rent_scatter(tab_value, selected_zip):
    if tab_value != "tab-rent" or not selected_zip:
        raise exceptions.PreventUpdate

    rent_scatterplot = create_rent_scatterplot(zip_code=selected_zip)
    rent_title = f"Median monthly rent over time in zip code {selected_zip}"

    return rent_scatterplot.to_dict(), rent_title


# tab4 :regression
@app.callback(
    [
        Output("reg-chart", "spec"),  # update
    ],
    [
        Input("tabs-content", "value"),
    ],
)
def update_regression(tab_value):

    if tab_value != "tab-reg":
        raise exceptions.PreventUpdate

    new_reg = create_reg_chart()

    return [new_reg.to_dict()]
