import plotly.express as px
from parse_utils import plot_color_list

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
                               title="Line plot of incomings and outgoings per day", 
                               color_discrete_sequence=plot_color_list)
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
                               title="Box plot of incomings and outgoings per day", 
                               color_discrete_sequence=plot_color_list)
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
                               title=f"Stacked Bar per {amount_column} Per Year/ Month", 
                               color_discrete_sequence=plot_color_list)
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    return fig