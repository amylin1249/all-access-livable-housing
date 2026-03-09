from dash import Dash, html, dcc, Input, Output, exceptions
import dash_bootstrap_components as dbc
from .visualize import (
    create_tract_map,
    create_reg_chart,
    create_rent_scatterplot,
    create_homeless_scatterplot,
    create_encampments_scatterplot,
)
import dash_vega_components as dvc
import calendar
import matplotlib

matplotlib.use("Agg")
from .datatypes import MERGED, CLEAN_ZILLOW
import pandas as pd

df_merged = pd.read_csv(MERGED)
all_tracts = sorted(df_merged["tract"].astype(str).str.zfill(11).unique())

try:
    df_zillow = pd.read_csv(CLEAN_ZILLOW)
    all_zips = sorted(df_zillow["zip"].astype(str).str.zfill(5).unique())
except Exception:
    all_zips = []

map_chart = create_tract_map(
    start_date="2020-01",
    end_date="2024-12",
    col_name="eviction_rate",
)

homeless_scatterplot = create_homeless_scatterplot(tract_id="tract_id")

encampments_scatterplot = create_encampments_scatterplot(tract_id="tract_id")


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
                    "This dashboard combines multiple data sources to provide a clearer picture of these trends. "
                    "Eviction rates and monthly median rent estimates help illustrate the pressures on housing affordability, "
                    "while citizen-reported encampments (311 service calls), city-reported encampments (official counts), and homeless population estimates "
                    "provide insights into patterns and concentrations of unhoused residents across the city. "
                    "Use the interactive features below to explore how these metrics vary across San Francisco's census tracts over time."
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
                        html.B("Eviction Rate"),
                        html.Br(),
                        f"{df_merged['eviction_rate'].mean():.2%}",
                    ],
                    style={"flex": "1", "textAlign": "center"},
                ),
                html.Div("|", style={"fontSize": "24px", "color": "#ddd"}),
                html.Div(
                    [
                        html.B("Average Rent"),
                        html.Br(),
                        f"${df_merged['median_rent'].mean():,.0f}",
                    ],
                    style={"flex": "1", "textAlign": "center"},
                ),
                html.Div("|", style={"fontSize": "24px", "color": "#ddd"}),
                html.Div(
                    [
                        html.B("311 Calls"),
                        html.Br(),
                        f"{df_merged['311_calls'].mean():,.0f}",
                    ],
                    style={"flex": "1", "textAlign": "center"},
                ),
                html.Div("|", style={"fontSize": "24px", "color": "#ddd"}),
                html.Div(
                    [
                        html.B("Homelessness Estimate"),
                        html.Br(),
                        f"{df_merged['estimate'].mean():,.0f}",
                    ],
                    style={"flex": "1", "textAlign": "center"},
                ),
            ],
            style={
                "display": "flex",
                "alignItems": "center",
                "padding": "20px",
                "margin": "20px 40px",
                "backgroundColor": "#f8f9fa",
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
                dcc.Tab(label="Regression Analysis", value="tab-reg"),
                dcc.Tab(label="Rent", value="tab-rent"),
                dcc.Tab(label="Homeless", value="tab-homeless"),
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
                html.Div(
                    [
                        html.Div(
                            [
                                html.B("Instruction: "),
                                "Use the ",
                                html.B("dropdown"),
                                " and ",
                                html.B("date selectors"),
                                " below to select your metric and time period of interest. The ",
                                html.B("map"),
                                " will update automatically based on your selection.",
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
                                    "label": "Homeless Population Estimate",
                                    "value": "estimate",
                                },
                                {"label": "Eviction Rate", "value": "eviction_rate"},
                                {"label": "Median Rent", "value": "median_rent"},
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
                        "backgroundColor": "#f9f9f9",
                        "borderRadius": "10px",
                        "marginBottom": "20px",
                    },
                ),
                # map
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
                        # "boxSizing": "border-box",
                    },
                ),
            ]
        )

    # [tab 2.regression]
    elif tab == "tab-reg":
        return html.Div(
            [
                html.Div(
                    [
                        html.H3(
                            id="regression-title",
                            style={"textAlign": "center", "color": "#2c3e50"},
                        ),
                        html.Hr(),
                        dvc.Vega(
                            id="reg-chart",
                            spec={},
                            style={"width": "100%", "height": "500px"},
                        ),
                    ],
                    style={
                        "width": "100%",
                        "padding": "20px",
                        "marginLeft": "20px",
                        "border": "1px solid #ddd",
                        "borderRadius": "10px",
                        "backgroundColor": "white",
                    },
                ),
            ],
            style={
                "display": "flex",
                "flexDirection": "row",
                "alignItems": "flex-start",
                "padding": "10px",
            },
        )

    # [tab 3. Rent Scatter Plot]
    elif tab == "tab-rent":
        return html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.B("Instruction: "),
                                "Explore the cmedian rent trends by zip code."
                                "The chart updates automatically based on your selection.",
                            ],
                            style={
                                "fontSize": "16px",
                                "lineHeight": "1.5",
                                "marginBottom": "20px",
                            },
                        ),
                        # dropdown
                        html.Label("Select Zip-code:", style={"fontWeight": "bold"}),
                        dcc.Dropdown(
                            id="zip-dropdown",
                            options=[
                                {"label": str(z), "value": str(z)} for z in all_zips
                            ],
                            value=all_zips[0] if all_zips else None,
                            clearable=False,
                        ),
                    ],
                    style={
                        "padding": "20px",
                        "backgroundColor": "#f9f9f9",
                        "borderRadius": "10px",
                        "marginBottom": "20px",
                    },
                ),
                # scatter plot
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

    # [tab 4. homeless scatter plot]
    else:
        return html.Div(
            [
                html.Div(
                    [
                        html.B("Analysis: "),
                        "Homelessness estimate : tents + vehicles + structures",
                        html.Br(),
                        html.Label("Select Tract ID:"),
                        dcc.Dropdown(
                            id="tract-dropdown",
                            options=[
                                {"label": str(t), "value": str(t)} for t in all_tracts
                            ],
                            value=all_tracts[0] if all_tracts else None,
                            clearable=False,
                            style={"width": "300px", "color": "black"},
                        ),
                    ],
                    style={
                        "padding": "20px",
                        "backgroundColor": "#f1f3f5",
                        "borderRadius": "10px",
                        "marginBottom": "30px",
                        "border": "1px solid #e9ecef",
                    },
                ),
                # scatter plots
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
        "311_calls": "311 calls",
        "eviction_rate": "Eviction rate",
        "median_rent": "Median rent",
        "tents": "Tents",
        "structures": "Structures",
        "vehicles": "Vehicles",
        "estimate": "Homelessness estimate",
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

    map_title = f"Average {METRIC_NAMES[selected_col].lower()} in SF tracts ({start_year}-{start_month} to {end_year}-{end_month})"

    return map_chart.to_dict(), map_title


# tab2 :regression
@app.callback(
    [
        Output("reg-chart", "spec"),  # update
        Output("regression-title", "children"),  # title-regression
    ],
    [
        Input("tabs-content", "value"),  # change in column
    ],
)
def update_regression(tab_value):

    if tab_value != "tab-reg":
        raise exceptions.PreventUpdate

    new_reg = create_reg_chart()
    reg_title = "Total Encampments Reported per Tract"

    return new_reg.to_dict(), reg_title


# tab3 : rent scatterplot
@app.callback(
    [Output("rent-scatter-plot", "spec"), Output("rent-plot-title", "children")],
    [Input("tabs-content", "value"), Input("zip-dropdown", "value")],
)
def update_rent_scatter(tab_value, selected_zip):
    if tab_value != "tab-rent" or not selected_zip:
        raise exceptions.PreventUpdate

    rent_scatterplot = create_rent_scatterplot(zip_code=selected_zip)
    rent_title = f"Median rent (per month) over time in zip code {selected_zip}"

    return rent_scatterplot.to_dict(), rent_title


# tab 4 : homeless scatterplot
@app.callback(
    [
        Output("homeless-1", "spec"),
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
    homeless_title1 = f"Homeless Population Estimate for Tract {selected_tract}"

    encampments_scatterplot = create_encampments_scatterplot(tract_id=selected_tract)
    encampment_title = f"City-reported encampments (official counts) over time in census tract {selected_tract}"

    return (
        homeless_scatterplot.to_dict(),
        homeless_title1,
        encampments_scatterplot.to_dict(),
        encampment_title,
    )


if __name__ == "__main__":
    app.run(debug=True)
