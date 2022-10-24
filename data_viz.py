import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import plotly.express as px

import pandas as pd

def show_line_plot(data: pd.DataFrame, 
                  amount_column: str,
                  date_column: str,
                  color_column: str,
                  hover_columns: list):
    
    plot_df = data.assign(**{date_column: lambda x: pd.to_datetime(x[date_column], format="%Y%m%d")})
    
    fig=px.line(plot_df,
                               x=date_column, 
                               y=amount_column, 
                               color=color_column, 
                               markers=True,
                            #    text=amount_column, 
                               hover_data=hover_columns,
                               width=1500, 
                               height=800, 
                               title="Line plot of incomings and outgoings per day")
    # fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    return fig

def show_box_plot(data: pd.DataFrame, 
                  amount_column: str,
                  date_column: str,
                  color_column: str,
                  hover_columns: list):
    
    plot_df = data.assign(**{date_column: lambda x: pd.to_datetime(x[date_column], format="%Y%m%d")})
    
    fig=px.box(plot_df,
                               x=date_column, 
                               y=amount_column, 
                               color=color_column, 
                            #    text=amount_column, 
                            #    hover_data=hover_columns,
                               width=1500, 
                               height=800, 
                               title="Box plot of incomings and outgoings per day")
    # fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    return fig

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
        )
    
    fig=px.bar(plot_df,
                               x="Year-Month", 
                               y=amount_column, 
                               color=color_column, 
                               text=amount_column, 
                               hover_data=hover_columns,
                               width=1500, 
                               height=800, 
                               title=f"Stacked Bar per {amount_column} Per Year/ Month")
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    return fig

def parse_input(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            try:
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            except:
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep=";")
            amount_column = df.filter(regex="EUR").columns.tolist()[0]
            if "Datum" in df.columns.tolist():
                groupby_column = "Mutatiesoort"
                date_column = "Datum"
                name_column = "Naam / Omschrijving"
                if "Saldo na mutatie" in df.columns.tolist():
                    sum_column = "Saldo na mutatie"
                else:
                    sum_column = None
            else:
                groupby_column = "Transaction type"
                date_column = "Date"
                name_column = "Name / Description"
                sum_column = "Balance Sum"
            
            df = df.assign(**{date_column: lambda x: pd.to_datetime(x[date_column], format="%Y%m%d"),
                                "Year": lambda x: x[date_column].dt.year,
                                "Month": lambda x: x[date_column].dt.month,
                                "Year-Month": lambda x: x["Year"].astype(str) + "-" +  x["Month"].astype(str),
                                amount_column: lambda d: d[amount_column]
                                # .str.replace(",",".")
                                .astype(float)})
            
            if "Datum" not in df.columns.tolist():
                df = df.assign(**{sum_column: lambda d: d[amount_column].cumsum()})
            else:
                df = df.assign(**{sum_column: lambda d: d[sum_column]
                                # .str.replace(",",".")
                                .astype(float)})
            return df, amount_column, groupby_column, date_column, name_column, sum_column
        else:
            return html.Div([
            'Currently only .csv files are accepted in this dashboard'
            ])
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

def parse_descriptives(contents, filename):
    df, amount_column, groupby_column, _, _, _ = parse_input(contents, filename)

    if "Af Bij" in df.columns.tolist():
        groupby_columns_list = [groupby_column, "Af Bij", amount_column]
        totals_columns_list = ["Year-Month", "Af Bij", amount_column]
    else:
        groupby_columns_list = [groupby_column, amount_column]
        totals_columns_list = ["Year-Month", amount_column]
    descriptives_df = (df[groupby_columns_list]
                    .groupby(groupby_columns_list[:-1])
                    .agg(["count", "mean", "median", "std", "min", "max"])
                    .sort_index()
                    .reset_index()
                    .round(2)
                    )
    descriptives_df.columns = [" - ".join(x) for x in descriptives_df.columns]
    head_df = df.head(2)
    totals_df = df[totals_columns_list].groupby(totals_columns_list[:-1]).sum().reset_index().round(2)
    
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
        
        html.H6("Total per month:"),

        dash_table.DataTable(
            totals_df.to_dict('records'),
            [{'name': i, 'id': i} for i in totals_df.columns]
        )
    ])

def parse_bar_plots(contents, filename):
    df, amount_column, groupby_column, date_column, name_column, _ = parse_input(contents, filename)

    bar_fig = show_bar_plot(data=df, 
                            amount_column=amount_column,
                            date_column=date_column,
                            color_column=groupby_column,
                            hover_columns=[name_column, groupby_column])
    if "Af Bij" in df.columns.tolist():
        bar_in_fig = show_bar_plot(data=df[df["Af Bij"]=="Bij"], 
                            amount_column=amount_column,
                            date_column=date_column,
                            color_column=groupby_column,
                            hover_columns=[name_column, groupby_column])
        bar_out_fig = show_bar_plot(data=df[df["Af Bij"]=="Af"], 
                            amount_column=amount_column,
                            date_column=date_column,
                            color_column=groupby_column,
                            hover_columns=[name_column, groupby_column])
        return html.Div([
                html.H5(filename),
                html.H6("Barplot of all incoming and outgoing transactions"),
                dcc.Graph(figure=bar_fig),
                html.H6("Barplot of all outgoing transactions"),
                dcc.Graph(figure=bar_out_fig),
                html.H6("Barplot of all incoming transactions"),
                dcc.Graph(figure=bar_in_fig)
            ])
    else:
        return html.Div([
            html.H5(filename),
            html.H6("Barplot of all incoming and outgoing transactions"),
            dcc.Graph(figure=bar_fig)
        ])
        
def parse_time_plots(contents, filename):
    df, amount_column, groupby_column, date_column, name_column, sum_column = parse_input(contents, filename)

    if "Af Bij" in df.columns.tolist():
        color_column = "Af Bij"
    else:
        color_column = None
    
    box_fig = show_box_plot(data=df, 
                            amount_column=amount_column,
                            date_column=date_column,
                            color_column=color_column,
                            hover_columns=[name_column, groupby_column])
    
    line_fig = show_line_plot(data=df, 
                            amount_column=amount_column,
                            date_column=date_column,
                            color_column=color_column,
                            hover_columns=[name_column, groupby_column])
     
    sum_line_fig = show_line_plot(data=df, 
                            amount_column=sum_column,
                            date_column=date_column,
                            color_column=None,
                            hover_columns=[name_column, groupby_column])
    if "Af Bij" in df.columns.tolist():
        return html.Div([
                html.H5(filename),
                html.H6("Boxplot of all incoming and outgoing transactions"),
                dcc.Graph(figure=box_fig),
                html.H6("Lineplot of all incoming and outgoing transactions"),
                dcc.Graph(figure=line_fig),
                html.H6("Lineplot of the sum of all incoming and outgoing transactions"),
                dcc.Graph(figure=sum_line_fig),
            ])
    else:
        return html.Div([
                html.H5(filename),
                html.H6("Boxplot of all incoming and outgoing transactions"),
                dcc.Graph(figure=box_fig),
                html.H6("Lineplot of all incoming and outgoing transactions"),
                dcc.Graph(figure=line_fig),
            ])
