import base64
import pandas as pd
import io
from dash import dcc, html, dash_table, Input, Output, State
from parse_utils_test import (ASN_column_names, 
                         ASN_column_subset,
                         ASN_DUTCH_TO_ENGLISH_dict,
                         BUNQ_column_subset,
                         BUNQ_TO_ING_names_dict,
                         ING_DUTCH_TO_ENGLISH_dict,
                         ING_DUTCH_columns_list,
                         ING_ENGLISH_columns_list)
from server_test import app

def parse_input(contents, filename, bank_string):
    
    print(bank_string)
    
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
            
            return df, amount_column, groupby_column #, date_column, name_column, sum_column
        else:
            return html.Div([
                'Currently only .csv files are accepted in this dashboard'
                ])
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
        
def parse_descriptives(contents, filename, bank_string):
    df, amount_column, groupby_column = parse_input(contents, filename, bank_string)

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
    totals_df = (df[totals_columns_list]
                 .groupby(totals_columns_list[:-1])
                 .sum()
                 .reset_index()
                 .round(2)
                 )
    
    return html.Div([
        html.H5(filename),
        html.H6("Data Frame Head"),

        dash_table.DataTable(
                        data=df.round(2).to_dict('records'),
                        columns=[{'name': i, 'id': i} for i in df.columns],
                        sort_action="native",
                        filter_action="native",
                        row_deletable=True,
                        export_format='csv',
                        export_headers='display',
                        merge_duplicate_headers=True,
                        page_size=10,
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
