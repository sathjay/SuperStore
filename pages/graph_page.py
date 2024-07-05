
import pandas as pd  # (version 1.0.0)
import plotly  # (version 4.5.4) pip install plotly==4.5.4
import plotly.express as px
import dash  # (version 1.9.1) pip install dash==1.9.1
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots


from index import app

from Functions.data_loader import load_and_preprocess_data, add_week_and_quarter
from Functions.USA_map import state_codes
from Functions.graph_page_functions import metrics_options, granularity_options, breakdown_options, filter_data, get_groupby_columns, aggregate_data

# File path to the Excel file
file_path = 'assets/Sample - Superstore.xlsx'
# Load and preprocess the data
sales_data, unique_years = load_and_preprocess_data(
    file_path)
# Add 'Week' and 'Quarter' columns
sales_data_with_q_info = add_week_and_quarter(sales_data)


graph_page_layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Label('Start Date:', className='date-label'),
            dcc.DatePickerSingle(
                id='start-date-picker',
                date=sales_data['Order Date'].min(),
                display_format='MMM D, YYYY'
            )
        ], width=3),

        dbc.Col([
            html.Label('End Date:', className='date-label'),
            dcc.DatePickerSingle(
                id='end-date-picker',
                date=sales_data['Order Date'].max(),
                display_format='MMM D, YYYY'
            )
        ], width=3),

        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Label('Select Granularity:', className='date-label')
                ], width=4),  # Adjust width as needed for the label
                dbc.Col([
                    dcc.Dropdown(
                        id='granularity-selector',
                        options=granularity_options,
                        value='Month'  # Default value
                    )
                ], width=8)  # Adjust width as needed for the dropdown
            ])
        ], width=3),

        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Label('Select Metric:', className='date-label')
                ], width=4),  # Adjust width as needed for the label
                dbc.Col([
                    dcc.Dropdown(
                        id='metric-selector',
                        options=metrics_options,
                        value='Profit'  # Default value
                    )
                ], width=8)  # Adjust width as needed for the dropdown
            ])
        ], width=3),


    ])
])


@app.callback(

    [
        Input('start-date-picker', 'date'),
        Input('end-date-picker', 'date'),
        Input('granularity-selector', 'value'),
        Input('metric-selector', 'value')])
def update_timeline_graph(start_date, end_date, granularity, selected_metric):
    # Filter and prepare data based on the selected dates and other inputs

    print(selected_metric, start_date, end_date, granularity)
    print(type(selected_metric), type(start_date),
          type(end_date), type(granularity))

    filtered_data = filter_data(
        sales_data_with_q_info, start_date, end_date, selected_metric, granularity)

    groupby_columns = get_groupby_columns(filtered_data, selected_metric)

    aggregate_data_for_chart = aggregate_data(
        filtered_data, groupby_columns, selected_metric)

    print(aggregate_data_for_chart)
