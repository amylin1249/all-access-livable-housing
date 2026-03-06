from pathlib import Path
from dash import Dash, html, dcc
from visualize import create_tract_map, create_scatterplot
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px


# Insert path later
MASTER_DATA = Path()

app = Dash()

# Incorporate data
df = pd.read_csv(MASTER_DATA)


# App layout
app.layout = [
    html.Div(children="Project All Access Livable Housing"),
    dag.AgGrid(
        rowData=df.to_dict("records"), columnDefs=[{"field": i} for i in df.columns]
    ),
    dcc.Graph(figure=px.histogram(df, x="continent", y="lifeExp", histfunc="avg")),
]


# # line graph
# fig = px.line(file, )


# #graph
# app.layout = html.Div([
#         html.H1(),
#         dag.AgGrid(
#             rowData = df.to_dict("")
#             columnDefs = [{"field": i} for i in df.columns]
#         ),
#         dcc.Graph(fifure=fig)
#     ])


if __name__ == "__main__":
    app.run(debug=True)
