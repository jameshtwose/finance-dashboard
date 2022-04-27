import base64
import datetime
import io
import dash
from dash.dependencies import Input, Output, State
# import dash_core_components as dcc
from dash import dcc
from dash import html
# import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
# import dash_table
import pandas as pd


app = dash.Dash()

server = app.server

app.layout = html.Div([
dcc.Upload(
        id='upload-data',
        children=html.Div([
        'Drag and Drop or ',
        html.A('Select Files')
        ]),
        style={
        'width': '100%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px'
         },
        # Allow multiple files to be uploaded
        multiple=True
),

html.Div(id='output-data-upload'),
])

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
        # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')),
                sep=";"
                )
        elif 'xls' in filename:
        # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
        
    plot_df = (df
            .assign(**{"Datum": lambda x: pd.to_datetime(x["Datum"], format="%Y%m%d"),
                    "Year": lambda x: x["Datum"].dt.year,
                    "Month": lambda x: x["Datum"].dt.month,
                    "Year-Month": lambda x: x["Year"].astype(str) + "-" +  x["Month"].astype(str),
                    "Day": lambda x: x["Datum"].dt.day,
                    "Amount": lambda x: x["Bedrag (EUR)"].str.replace(",", ".").astype(float),
                    })
            .drop(["Tag", "Saldo na mutatie", "Bedrag (EUR)"], axis=1)
        )

    fig=px.bar(plot_df[plot_df["Af Bij"]=="Af"], 
                               x="Year-Month", 
                               y="Amount", 
                               color="Code", 
                               text="Amount", 
                               hover_data=['Naam / Omschrijving', "Mutatiesoort"],
                               width=1500, 
                               height=800, 
                               title="Stacked Bar per Code")
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.add_hline(y=2926, line_dash="dot", 
                #   line_color="white",
                #   annotation_font_color="white",
                annotation_font_size=20,
                annotation_text="Main Income",
                annotation_position="top left")
    
    return html.Div([
                    dcc.Graph(figure=fig)
                    ])

@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

if __name__ == '__main__':
    app.run_server(debug=True)