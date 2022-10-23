import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import plotly.express as px

import pandas as pd

def show_bar_plot(data: pd.DataFrame, 
                  amount_column: str,
                  date_column: str,
                  color_column: str,
                  hover_columns: list):
    
    plot_df = (data
            .assign(**{date_column: lambda x: pd.to_datetime(x[date_column], format="%Y%m%d"),
                    "Year": lambda x: x[date_column].dt.year,
                    "Month": lambda x: x[date_column].dt.month,
                    "Year-Month": lambda x: x["Year"].astype(str) + "-" +  x["Month"].astype(str),
                    "Day": lambda x: x[date_column].dt.day,
                    # "Amount": lambda x: x[amount_column].str.replace(",", ".").astype(float),
                    })
            # .drop(["Tag", "Saldo na mutatie", "Bedrag (EUR)"], axis=1)
        )
    
    fig=px.bar(plot_df,
        # plot_df[plot_df["Af Bij"]=="Af"], 
                               x="Year-Month", 
                               y=amount_column, 
                               color=color_column, 
                               text=amount_column, 
                               hover_data=hover_columns,
                               width=1500, 
                               height=800, 
                               title=f"Stacked Bar per {amount_column} Per Year/ Month")
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.add_hline(y=2926, line_dash="dot", 
                #   line_color="white",
                #   annotation_font_color="white",
                annotation_font_size=20,
                annotation_text="Main Income",
                annotation_position="top left")
    return fig

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    amount_column = df.filter(regex="EUR").columns.tolist()[0]
    groupby_column = "Transaction type"
    df = df.assign(**{amount_column: lambda d: d[amount_column]
                      .str.replace(",",".")
                      .astype(float)})
    descriptives_df = (df[[groupby_column, amount_column]]
                       .groupby(groupby_column)
                    #    .describe()
                       .agg(["count", "mean", "median", "std", "min", "max"])
                       .reset_index()
                       )
    descriptives_df.columns = [" - ".join(x) for x in descriptives_df.columns]
    head_df = df.head(2)
    
    bar_fig = show_bar_plot(data=df, 
                            amount_column=amount_column,
                            date_column="Date",
                            color_column=groupby_column,
                            hover_columns=['Name / Description', "Transaction type"])
    
    return html.Div([
        html.H5(filename),
        html.H6("Data Frame Head"),

        dash_table.DataTable(
            head_df.to_dict('records'),
            [{'name': i, 'id': i} for i in head_df.columns]
        ),
        
        html.H6("Descriptive Statistics:"),

        dash_table.DataTable(
            descriptives_df.to_dict('records'),
            [{'name': i, 'id': i} for i in descriptives_df.columns]
        ),
        
        dcc.Graph(figure=bar_fig)

    ])
