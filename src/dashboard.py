from dash import Dash, html, dcc, Input, Output, dash
import dash_bootstrap_components as dbc
from .visualize import create_tract_map, create_reg_chart
import dash_vega_components as dvc
import calendar
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from .datatypes import MERGED

my_chart = create_tract_map(
    source_file=MERGED,
    start_date="2020-01",
    end_date="2024-12",
    col_name="eviction_rate",
    agg="mean",
)

app = Dash(__name__, external_stylesheets=[dbc.themes.MORPH])

app.layout = html.Div(
    [
        html.H1(
            "San Francisco Housing & Homelessness Dashboard",
            className="mt-4",
            style={"textAlign": "center", "color": "#2c3e50"},
        ),
        # one line in between
        html.Br(),
        # text
        html.Div(
            [
                html.Hr(),  # Horizontal line
                html.P(
                    "San Francisco has experienced significant changes in housing and homelessness over the past several years. "
                    "Many factors, including rising rents and increased evictions, have contributed to a growing number of unhoused individuals across the city. "
                    "This dashboard combines multiple data sources to provide a clearer picture of these trends. "
                    "Eviction rates and monthly median rent estimates help illustrate the pressures on housing affordability, "
                    "while citizen-reported encampments (311 service calls), city-reported encampments (official counts), and homeless population estimates "
                    "provide insights into patterns and concentrations of unhoused residents across the city. "
                    "Use the interactive features below to explore how these metrics vary across San Francisco's census tracts over time."
                ),
                html.P(
                    [
                        "Use the ",
                        html.B("dropdown"),
                        " and ",
                        html.B("date selectors"),
                        " below to select your metric and time period of interest. The ",
                        html.B("map"),
                        " will update automatically based on your selection.",
                    ],
                    style={"fontSize": "16px", "lineHeight": "1.5"},
                ),
                html.Hr(),  # Horizontal line
            ],
            style={"padding": "10px 40px", "color": "#34495e"},
        ),
        # data select dropdown
        html.Div(
            [
                html.Label("Select Metric:"),
                dcc.Dropdown(
                    id="column-dropdown",
                    options=[
                        {"label": "Homeless Population Estimate", "value": "estimate"},
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
                # one line in between
                html.Br(),
                # date select dropdown
                html.Div(
                    [
                        # Start date
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
                                    style={"width": "120px", "display": "inline-block"},
                                ),
                            ],
                            style={"display": "inline-block"},
                        ),
                        # end date
                        html.Div(
                            [
                                html.Label("End Period:", style={"marginLeft": "30px"}),
                                
                                dcc.Dropdown(
                                    id="end-month",
                                    options=[
                                        {
                                            "label": calendar.month_name[m],
                                            "value": f"{m:02d}",
                                        }
                                        for m in range(1, 13)
                                    ],
                                    value="02",
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
                                    value="2020",
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
            style={"padding": "20px", "backgroundColor": "#f9f9f9"},
        ),
        html.Div(
            [
                # left : map
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
                "height": "500px",  # fixed height
                "borderRadius": "10px",
            },
        ),
    ],
    style={
        "width": "50%",
        "padding": "20px",
        "border": "1px solid #ddd",
        "borderRadius": "10px",
        "backgroundColor": "white",
        "boxSizing": "border-box",
    },
),
                # right : regression chart
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
                        "width": "50%",
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
        ),
    ],
    style={"maxWidth": "1200px", "margin": "0 auto"},
)


@app.callback(
    [
        Output("sf-map", "spec"),  # update
        Output("map-title", "children"),  # title-map
        Output("reg-chart", "spec"),  # update
        Output("regression-title", "children"),
    ],  # title-regression
    [
        Input("column-dropdown", "value"),  # change in column
        Input("start-year", "value"),  # change in start-date
        Input("start-month", "value"),
        Input("end-year", "value"),  # change in end-date
        Input("end-month", "value"),
    ],
)
def update_dashboard(selected_col, start_year, start_month, end_year, end_month):

    if any(
        v is None for v in [selected_col, start_year, start_month, end_year, end_month]
    ):
        raise dash.exceptions.PreventUpdate

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
        source_file=MERGED,
        start_date=start_dt,
        end_date=end_dt,
        col_name=selected_col,
        agg="mean",
    )

    map_title = f"Average {METRIC_NAMES[selected_col].lower()} in SF tracts ({start_year}-{start_month} to {end_year}-{end_month})"

    new_reg = create_reg_chart()
    reg_title = f"Total Encampments Reported per Tract"

    return map_chart.to_dict(), map_title, new_reg.to_dict(), reg_title


if __name__ == "__main__":
    app.run(debug=True)
