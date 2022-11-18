from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "30rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "30rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Finance Dashboard", className="display-4"),
        html.Hr(),
        html.P(
            """Upload your finance data in csv format (currently ING .csv 
            files in either English or Dutch are accepted)""", 
            className="lead"
        ),
        html.Hr(),
        dcc.Dropdown(options=["ASN",
                              "BUNQ",
                              "ING - Dutch (comma seperated)", 
                              "ING - Dutch (semicolon seperated)", 
                              "ING - English (comma seperated)", 
                              "ING - English (semicolon seperated)"], 
                     value="ASN",
                     multi=False, 
                     id='bank-string-dropdown'),
        html.Hr(),
        dcc.Upload(html.Button('Upload File'), id='upload-data', multiple=True),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home/ Descriptives", href="/", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div([html.Div(id='output-data-upload')], id="page-content", 
                   style=CONTENT_STYLE)