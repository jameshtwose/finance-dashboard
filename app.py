from server import app, server
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from sidebar import sidebar, content
from parse import parse_descriptives, parse_bar_plots, parse_time_plots
import pandas as pd

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(Output('output-data-upload-descriptives', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              Input('bank-string-dropdown', 'value'))
def update_descriptives_output(list_of_contents, list_of_names, bank_string):
    if list_of_contents is not None:
        children = parse_descriptives(contents=list_of_contents[0],
                                      filename=list_of_names[0],
                                      bank_string=bank_string)
        return children
    
@app.callback(Output('output-data-upload-bar', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              Input('bank-string-dropdown', 'value'))
def update_bar_plots_output(list_of_contents, list_of_names, bank_string):
    if list_of_contents is not None:
        children = parse_bar_plots(contents=list_of_contents[0],
                                      filename=list_of_names[0],
                                      bank_string=bank_string)
        return children
    
@app.callback(Output('output-data-upload-time', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              Input('bank-string-dropdown', 'value'))
def update_time_plots_output(list_of_contents, list_of_names, bank_string):
    if list_of_contents is not None:
        children = parse_time_plots(contents=list_of_contents[0],
                                      filename=list_of_names[0],
                                      bank_string=bank_string)
        return children

@app.callback(Output("page-content", "children"), 
              [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        # return html.P("This is the content of the home page!")
        output = html.Div([html.Div(id='output-data-upload-descriptives'), 
                           html.Div(id='dd-output-container')])
        return output
    elif pathname == "/page-1":
        # return html.P("This is the content of page 1. Yay!")
        return html.Div(id='output-data-upload-bar')
    elif pathname == "/page-2":
        # return html.P("Oh cool, this is page 2!")
        return html.Div(id='output-data-upload-time')
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
    # app.run_server(debug=False, threaded=False)