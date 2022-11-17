import os
import pandas as pd
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

df = pd.read_csv("data/NL20INGB0679269126_01-07-2022_23-10-2022.csv", sep=",", decimal=",")

country_list = df["Mutatiesoort"].unique().tolist()

app.layout = html.Div([
    html.H1(id='H1', children='COVID Numbers', style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),
    html.Div([dcc.Dropdown(
            id='country_choice',
            options=[{'label': i.title().replace("_", " "), 'value': i} for i in country_list],
            value=country_list[0]
        )], style={'width': '20%', 'display': 'inline-block', "padding": "5px"}),
    html.Div(id='table'),
    html.Div(html.A(children="Created by James Twose",
                    href="https://services.jms.rocks",
                    style={'color': "#743de0"}),
                    style = {'textAlign': 'center',
                             'color': "#743de0",
                             'marginTop': 40,
                             'marginBottom': 40})
]
)

@app.callback(Output(component_id='table', component_property='children'),
              [Input(component_id='country_choice', component_property='value')]
              )
def table_update(country_choice):
    
    descriptives_df = (df.loc[df["Mutatiesoort"] == '{}'.format(country_choice), :]
                       .describe())
    
    descriptives_table = dash_table.DataTable(
            descriptives_df.to_dict('records'),
            [{'name': i, 'id': i} for i in descriptives_df.columns]
        )
    
    return html.Div([descriptives_table])


if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
    # app.run_server(debug=False, threaded=False)