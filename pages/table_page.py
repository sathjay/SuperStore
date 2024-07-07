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

from index import app
from Functions.data_loader import load_and_preprocess_data, add_week_and_quarter

# File path to the Excel file
file_path = 'assets/Sample - Superstore.xlsx'
# Load and preprocess the data
sales_data, unique_years = load_and_preprocess_data(
    file_path)
# Add 'Week' and 'Quarter' columns
sales_data_with_q_info = add_week_and_quarter(sales_data)


table_page_layout = html.Div([

    dbc.Row([html.P('SuperStore Data', className='table-heading')],
            className='table-heading-row'),

    dbc.Row([

        dbc.Col([


        ], className='table-display', width=10),

        dbc.Col([

            dbc.Row([


            ], className='table-filter-row '),

            dbc.Row([

                html.P('Filter by Geography:',
                       className='table-filter-heading'),

                dbc.Row([dbc.Row([
                    html.Label('Region:', className='bubble-chart-input-label')
                ]),
                    dbc.Row([
                        dcc.Dropdown(
                            id='region-dropdown',
                            options=[{'label': 'All', 'value': 'All'}] +
                            [{'label': region, 'value': region}
                                for region in sales_data_with_q_info['Region'].unique()],
                            value='All',  # Default to 'All'
                            placeholder="Select a Region"
                        ),
                    ])
                ], className='table-filter-container'),

                dbc.Row([dbc.Row([
                    html.Label('State:', className='bubble-chart-input-label')
                ]),
                    dbc.Row([
                        dcc.Dropdown(
                            id='state-dropdown',
                            options=[],
                            value=None,
                            placeholder="Select a State",
                            disabled=True  # Initially disabled

                        ),
                    ])
                ], className='table-filter-container'),

                dbc.Row([
                    dbc.Row([
                        html.Label(
                            'City:', className='bubble-chart-input-label')
                    ]),
                    dbc.Row([
                        dcc.Dropdown(
                            id='city-dropdown',
                            options=[],
                            value=None,
                            placeholder="Select a City",
                            disabled=True  # Initially disabled
                        ),
                    ])
                ], className='table-filter-container'),

            ], className='table-filter-row'),

        ], className='table-data-filter', width=2)

    ])

])


@app.callback(
    [
        Output('state-dropdown', 'options'),
        Output('state-dropdown', 'disabled'),
        Output('city-dropdown', 'options'),
        Output('city-dropdown', 'disabled')
    ],
    [
        Input('region-dropdown', 'value'),
        Input('state-dropdown', 'value')
    ]
)
def update_dropdowns(selected_region, selected_state):
    if selected_region == 'All':
        # If "All" is selected in the region dropdown, disable state and city dropdowns and clear options
        return [], True, [], True

    # Update the state dropdown options based on the selected region
    states = sales_data_with_q_info[sales_data_with_q_info['Region']
                                    == selected_region]['State'].unique()
    state_options = [{'label': state, 'value': state} for state in states]

    if not selected_state or selected_state not in states:
        # If no state is selected or the selected state is not valid, disable city dropdown
        return state_options, False, [], True

    # Update the city dropdown options based on the selected state
    cities = sales_data_with_q_info[sales_data_with_q_info['State']
                                    == selected_state]['City'].unique()
    city_options = [{'label': city, 'value': city} for city in cities]

    return state_options, False, city_options, False
