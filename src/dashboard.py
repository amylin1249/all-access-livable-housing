from dash import Dash, html, doc
import pandas as pd
import plotly.express as px
#import dash_ag_grid as dag





#dataframe 

file = pd.DataFrame()
        pd.read_csv(".csv")


# line graph
fig = px.line(file, )



app = Dash(__name__) 


#graph
app.layout = html.Div([
        html.H1(),
        dag.AgGrid(
            rowData = df.to_dict("")
            columnDefs = [{"field": i} for i in df.columns]
        ),
        dcc.Graph(fifure=fig)



    ])




#running dash
if __name__ == '__main__':
    app.run(debug=True)

