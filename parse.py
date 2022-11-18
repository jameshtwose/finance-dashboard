import base64
import pandas as pd
import io
from dash import dcc, html, dash_table, Input, Output
from data_viz import (show_bar_plot,
                      show_line_plot,
                      show_box_plot)
from parse_utils import (ASN_column_names, 
                         ASN_column_subset,
                         ASN_DUTCH_TO_ENGLISH_dict,
                         BUNQ_column_subset,
                         BUNQ_TO_ING_names_dict,
                         ING_DUTCH_TO_ENGLISH_dict,
                         ING_DUTCH_columns_list,
                         ING_ENGLISH_columns_list)
from server import app

selection_list = ["ASN",
"BUNQ",
"ING - Dutch (comma seperated)", 
"ING - Dutch (semicolon seperated)", 
"ING - English (comma seperated)", 
"ING - English (semicolon seperated)"]

@app.callback(
    Output('df', 'children'),
    Output('amount_column', 'children'),
    Output('groupby_column', 'children'),
    Output('date_column', 'children'),
    Output('name_column', 'children'),
    Output('sum_column', 'children'),
    Input('num-multi', 'value'))
def parse_input(contents, filename, bank_string=selection_list[5]):
    
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    
    try:
        if 'csv' in filename:
    
            if bank_string == "ASN":
                df = (pd.read_csv(io.StringIO(decoded.decode('utf-8')),
                                header=None, 
                                names=ASN_column_names, 
                                sep=",", 
                                decimal=".")
                      .loc[:, ASN_column_subset]
                      .rename(columns=ASN_DUTCH_TO_ENGLISH_dict)
                      .assign(**{"Debit/credit": lambda d: d["Amount (EUR)"]
                                 .mask(lambda x: x > 0, 1)
                                 .mask(lambda x: x < 0, 0)
                                 .replace({0: "Debit", 1: "Credit"}),
                                 "Amount (EUR)": lambda d: d["Amount (EUR)"].abs(),
                                 "Date": lambda d: pd.to_datetime(d["Date"], format="%d-%m-%Y")
                                 }
                              )
                      )
            elif bank_string == "BUNQ":
                df = (pd.read_csv(io.StringIO(decoded.decode('utf-8')))
                    .assign(**{"Amount": lambda d: d["Amount"]
                                .str.replace(".", "")
                                .str.replace(",",".")
                                .astype(float)})
                       .loc[:, BUNQ_column_subset]
                      .rename(columns=BUNQ_TO_ING_names_dict)
                      .assign(**{"Debit/credit": lambda d: d["Amount (EUR)"]
                                 .mask(lambda x: x > 0, 1)
                                 .mask(lambda x: x < 0, 0)
                                 .replace({0: "Debit", 1: "Credit"}),
                                 "Amount (EUR)": lambda d: d["Amount (EUR)"].abs(),
                                 "Date": lambda d: pd.to_datetime(d["Date"], format="%Y-%m-%d"),
                                 "Code": "Not Available"
                                 }
                              )
                    )
            elif bank_string == "ING - Dutch (comma seperated)":
                df = (pd.read_csv(io.StringIO(decoded.decode('utf-8')), 
                                sep=",", 
                                decimal=",")
                      .loc[:, ING_DUTCH_columns_list]
                      .assign(**{"Af Bij": lambda d: d["Af Bij"]
                                 .str.replace("Af", "Debit")
                                 .str.replace("Bij", "Credit")
                                 })
                      .rename(columns=ING_DUTCH_TO_ENGLISH_dict)
                      )
            elif bank_string == "ING - Dutch (semicolon seperated)":
                df = (pd.read_csv(io.StringIO(decoded.decode('utf-8')), 
                                sep=";", 
                                decimal=",")
                      .loc[:, ING_DUTCH_columns_list]
                      .assign(**{"Af Bij": lambda d: d["Af Bij"]
                                 .str.replace("Af", "Debit")
                                 .str.replace("Bij", "Credit")
                                 })
                      .rename(columns=ING_DUTCH_TO_ENGLISH_dict)
                      )
            elif bank_string == "ING - English (comma seperated)":
                df = (pd.read_csv(io.StringIO(decoded.decode('utf-8')), 
                                sep=",", 
                                decimal=",")
                      .loc[:, ING_ENGLISH_columns_list]
                      )
            elif bank_string == "ING - English (semicolon seperated)":
                df = (pd.read_csv(io.StringIO(decoded.decode('utf-8')), 
                                sep=";", 
                                decimal=",")
                      .assign(**{"Amount (EUR)": lambda d: d["Amount (EUR)"]
                                .str.replace(".", "")
                                .str.replace(",",".")
                                .astype(float)})
                      .loc[:, ING_ENGLISH_columns_list]
                      )
                            
            amount_column = 'Amount (EUR)'
            groupby_column = 'Code'
            date_column = 'Date'
            name_column = 'Name / Description'
            sum_column = 'Total (EUR)'
            
            if "ING" in bank_string:
                df = df.assign(**{date_column: lambda x: pd.to_datetime(x[date_column], format="%Y%m%d")})
            
            df = df.assign(**{"Year": lambda x: x[date_column].dt.year,
                                "Month": lambda x: x[date_column].dt.month,
                                "Year-Month": lambda x: x["Year"].astype(str) + "-" +  x["Month"].astype(str)
                                })
            
            if bank_string != "ASN":
                df = (df
                      .sort_values(by=date_column)
                      .assign(**{sum_column: lambda d: d["Amount (EUR)"]
                            .where(df["Debit/credit"] == "Credit", -d["Amount (EUR)"])
                            .cumsum()
                            }
                        )
                      )
            
            print(df.head(10))
            
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
        

# def parse_input(contents, filename):
    
#     content_type, content_string = contents.split(',')

#     decoded = base64.b64decode(content_string)
#     try:
#         if 'csv' in filename:
#             # Assume that the user uploaded a CSV file
#             try:
#                 df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
#                 # print(df.head())
#             except:
#                 df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep=";")
#                 # print(df.head())
#             amount_column = df.filter(regex="EUR").columns.tolist()[0]
#             if "Datum" in df.columns.tolist():
#                 groupby_column = "Mutatiesoort"
#                 date_column = "Datum"
#                 name_column = "Naam / Omschrijving"
#                 # df = df.assign(**{"Bedrag (EUR)": lambda d: d["Bedrag (EUR)"].str.replace(",", ".").astype(float)})
#                 if "Saldo na mutatie" in df.columns.tolist():
#                     sum_column = "Saldo na mutatie"
#                 else:
#                     sum_column = None
#             else:
#                 groupby_column = "Transaction type"
#                 date_column = "Date"
#                 name_column = "Name / Description"
#                 sum_column = "Balance Sum"
            
#             df = df.assign(**{date_column: lambda x: pd.to_datetime(x[date_column], format="%Y%m%d"),
#                                 "Year": lambda x: x[date_column].dt.year,
#                                 "Month": lambda x: x[date_column].dt.month,
#                                 "Year-Month": lambda x: x["Year"].astype(str) + "-" +  x["Month"].astype(str),
#                                 amount_column: lambda d: d[amount_column]
#                                 # .str.replace(",",".")
#                                 .astype(float)})
            
#             if "Datum" not in df.columns.tolist():
#                 df = df.assign(**{sum_column: lambda d: d[amount_column].cumsum()})
#             else:
#                 df = df.assign(**{sum_column: lambda d: d[sum_column]
#                                 # .str.replace(",",".")
#                                 .astype(float)})
#             return df, amount_column, groupby_column, date_column, name_column, sum_column
#         else:
#             return html.Div([
#             'Currently only .csv files are accepted in this dashboard'
#             ])
#     except Exception as e:
#         print(e)
#         return html.Div([
#             'There was an error processing this file.'
#         ])

def parse_descriptives(contents, filename):
    df, amount_column, groupby_column, _, _, _ = parse_input(contents, filename)

    groupby_columns_list = [groupby_column, "Debit/credit", amount_column]
    totals_columns_list = ["Year-Month", "Debit/credit", amount_column]

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

    bar_in_fig = show_bar_plot(data=df[df["Debit/credit"]=="Credit"], 
                        amount_column=amount_column,
                        date_column=date_column,
                        color_column=groupby_column,
                        hover_columns=[name_column, groupby_column])
    bar_out_fig = show_bar_plot(data=df[df["Debit/credit"]=="Debit"], 
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

        
def parse_time_plots(contents, filename):
    df, amount_column, groupby_column, date_column, name_column, sum_column = parse_input(contents, filename)
   
    color_column = "Debit/credit"
    
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
    return html.Div([
            html.H5(filename),
            html.H6("Boxplot of all incoming and outgoing transactions"),
            dcc.Graph(figure=box_fig),
            html.H6("Lineplot of all incoming and outgoing transactions"),
            dcc.Graph(figure=line_fig),
            html.H6("Lineplot of the sum of all incoming and outgoing transactions"),
            dcc.Graph(figure=sum_line_fig),
        ])

