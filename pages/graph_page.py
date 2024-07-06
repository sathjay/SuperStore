
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
from Functions.graph_page_functions import metrics_options, granularity_options, breakdown_options, filter_data, aggregate_data_for_timeline_graph, bubble_chart_dataframe

# File path to the Excel file
file_path = 'assets/Sample - Superstore.xlsx'
# Load and preprocess the data
sales_data, unique_years = load_and_preprocess_data(
    file_path)
# Add 'Week' and 'Quarter' columns
sales_data_with_q_info = add_week_and_quarter(sales_data)
metrics_list = ['Days to Ship', 'Discount',
                'Profit', 'Quantity', 'Sales', 'Returned']


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

    ]),

    dbc.Row([
        dbc.Col([], width=5),
        dbc.Col([], width=5),


        dbc.Col([
            dbc.Row([dbc.Row([
                    html.Label('X-Axis', className='date-label')
                    ]),
                dbc.Row([
                    dcc.Dropdown(
                        id='x-axis-dropdown',
                        options=metrics_options,
                        value="Sales"
                    ),
                ])
            ]),

            dbc.Row([dbc.Row([
                    html.Label('Y-Axis', className='date-label')
                    ]),
                dbc.Row([
                    dcc.Dropdown(
                        id='y-axis-dropdown',
                        options=metrics_options,
                        value="Profit"
                    ),
                ])

            ]),
            dbc.Row([
                dbc.Row([
                    html.Label('Breakdown:', className='date-label')
                ]),
                dbc.Row([
                    dcc.Dropdown(
                        id='breakdown',
                        options=breakdown_options,
                        value="Category"
                    ),
                ])
            ]),

        ], width=2)

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

    filtered_data, agg_list = filter_data(
        sales_data_with_q_info, start_date, end_date, selected_metric, granularity)

    time_line_df = aggregate_data_for_timeline_graph(
        filtered_data, agg_list, selected_metric)

    print(time_line_df)


@app.callback(
    [Output('x-axis-dropdown', 'options'),
     Output('y-axis-dropdown', 'options')],
    [Input('x-axis-dropdown', 'value'),
     Input('y-axis-dropdown', 'value')]
)
def update_dropdowns(x_selected, y_selected):
    if x_selected:
        y_options = [
            option for option in metrics_options if option['value'] != x_selected]
    else:
        y_options = metrics_options

    if y_selected:
        x_options = [
            option for option in metrics_options if option['value'] != y_selected]
    else:
        x_options = metrics_options

    return x_options, y_options


@app.callback(

    [
        Input('start-date-picker', 'date'),
        Input('end-date-picker', 'date'),
        Input('metric-selector', 'value'),
        Input('x-axis-dropdown', 'value'),
        Input('y-axis-dropdown', 'value'),
        Input('breakdown', 'value'),
    ])
def update_bubble_chart(start_date, end_date, selected_metric, x_axis, y_axis, breakdown):

    bubble_chart_df = bubble_chart_dataframe(
        sales_data, start_date, end_date, selected_metric, metrics_list, breakdown)

    print("This is the bubble chart dataframe:")
    print(bubble_chart_df)
