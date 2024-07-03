import pandas as pd  # (version 1.0.0)
import plotly  # (version 4.5.4) pip install plotly==4.5.4
import plotly.express as px
import dash  # (version 1.9.1) pip install dash==1.9.1
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from index import app
from Functions.data_loader import load_and_preprocess_data
from Functions.USA_map import state_codes


# File path to the Excel file
file_path = 'assets/Sample - Superstore.xlsx'
# Load and preprocess the data
sales_data, unique_years = load_and_preprocess_data(
    file_path)


home_page_layout = html.Div([

    dbc.Row([
        dbc.Col(html.H1("Sales Summary"), className='title', width=12)
    ]),

    dbc.Row([
        dbc.Col(html.Div([

            # Placeholder for graph or map
            dcc.Graph(id='main-graph', style={'height': '90vh'}),
        ]), width=10),  # 75% width

        dbc.Col(html.Div([
            html.H4("Controls", className="text-center"),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': str(year), 'value': year}
                         for year in unique_years],
                placeholder="Select a year",
                style={'width': '100%', 'padding': '10px'}
            ),
            dcc.Dropdown(
                id='state-dropdown',
                # Assuming state_codes is already defined or imported
                options=[{'label': state, 'value': code}
                         for state, code in state_codes.items()],
                placeholder="Select a state",
                style={'width': '100%', 'padding': '10px'}
            ),
            html.Div(id='display-selected-state')
        ]), width=2),  # 25% width
    ])
])


@app.callback(
    Output('display-selected-state', 'children'),
    [Input('year-dropdown', 'value'),
     Input('state-dropdown', 'value')]
)
def display_selected(year, state_code):
    if year and state_code:
        return f'You have selected the year {year} and state {state_code}.'
    elif year:
        return f'You have selected the year {year}.'
    elif state_code:
        return f'You have selected the state {state_code}.'
    return "Please select a year and a state."
