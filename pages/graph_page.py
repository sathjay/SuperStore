
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
from Functions.graph_page_functions import metrics_options, granularity_options, breakdown_options, filter_data, aggregate_data_for_timeline_graph, bubble_chart_dataframe, create_bubble_chart, create_combined_date_column, create_line_chart

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
            dbc.Row([
                html.Label('Start Date:', className='linechart-input-label',
                           )]),
            dbc.Row([
                dcc.DatePickerSingle(
                    id='start-date-picker',
                    date=sales_data['Order Date'].min(),
                    display_format='MMM D, YYYY',
                    className='custom-datepicker'
                )
            ], className='linechart-input-field')
        ], width=3, className='linechart-input-container'),

        dbc.Col([
            dbc.Row([
                html.Label('End Date:', className='linechart-input-label',
                           )]),
            dbc.Row([
                dcc.DatePickerSingle(
                    id='end-date-picker',
                    date=sales_data['Order Date'].max(),
                    display_format='MMM D, YYYY',
                    className='custom-datepicker'
                )
            ], className='linechart-input-field')
            # Padding around the column content
        ], width=3, className='linechart-input-container'),

        dbc.Col([
            dbc.Row([
                html.Label('Select Period:', className='linechart-input-label',
                           )]),
            dbc.Row([
                dcc.Dropdown(
                    id='granularity-selector',
                    options=granularity_options,
                    value='Quarter',  # Default value
                    clearable=False
                )], className='linechart-input-field')
            # Padding around the column content
        ], width=3, className='linechart-input-container'),

        dbc.Col([
            dbc.Row([
                html.Label('Select Metric:', className='linechart-input-label',
                           )]),
            dbc.Row([
                dcc.Dropdown(
                    id='metric-selector',
                    options=metrics_options,
                    value='Sales',  # Default value
                    clearable=False
                )], className='linechart-input-field')
            # Padding around the column content
        ], width=3, className='linechart-input-container')


    ], className='timeline-chart-input-row'),

    dbc.Row([
        dbc.Col(
            [dcc.Graph(id='timeline-chart', config={'displayModeBar': False})], className='graph-page-chart', width=5),
        dbc.Col(
            [dcc.Graph(id='bubble-chart', config={'displayModeBar': False})], className='graph-page-chart', width=5),

        dbc.Col([
            dbc.Row([dbc.Row([
                    html.Label('X-Axis:', className='bubble-chart-input-label')
                    ]),
                dbc.Row([
                    dcc.Dropdown(
                        id='x-axis-dropdown',
                        options=metrics_options,
                        value="Profit",
                        clearable=False
                    ),
                ])
            ], className='bubble-chart-input-container'),

            dbc.Row([dbc.Row([
                    html.Label('Y-Axis:', className='bubble-chart-input-label')
                    ]),
                dbc.Row([
                    dcc.Dropdown(
                        id='y-axis-dropdown',
                        options=metrics_options,
                        value="Profit Ratio",
                        clearable=False
                    ),
                ])
            ], className='bubble-chart-input-container'),

            dbc.Row([
                dbc.Row([
                    html.Label(
                        'Breakdown:', className='bubble-chart-input-label')
                ]),
                dbc.Row([
                    dcc.Dropdown(
                        id='breakdown',
                        options=breakdown_options,
                        value="Sub-Category",
                        clearable=False
                    ),
                ])
            ], className='bubble-chart-input-container'),

        ], className='bubble-chart-control', width=2)

    ], className='graphpage-graph-row')
])


@app.callback(
    Output('timeline-chart', 'figure'),
    [
        Input('start-date-picker', 'date'),
        Input('end-date-picker', 'date'),
        Input('granularity-selector', 'value'),
        Input('metric-selector', 'value')])
def update_timeline_graph(start_date, end_date, granularity, selected_metric):
    '''Update the timeline graph based on the selected inputs.'''
    # Filter and prepare data based on the selected dates and other inputs

    print(selected_metric, start_date, end_date, granularity)
    print(type(selected_metric), type(start_date),
          type(end_date), type(granularity))

    filtered_data, agg_list = filter_data(
        sales_data_with_q_info, start_date, end_date, selected_metric, granularity)

    time_line_df = aggregate_data_for_timeline_graph(
        filtered_data, agg_list, selected_metric)

    time_line_df = create_combined_date_column(time_line_df)

    timeline_chart_fig = create_line_chart(time_line_df, selected_metric)

    print(time_line_df)

    return timeline_chart_fig


@app.callback(
    [Output('x-axis-dropdown', 'options'),
     Output('y-axis-dropdown', 'options')],
    [Input('x-axis-dropdown', 'value'),
     Input('y-axis-dropdown', 'value')]
)
def update_dropdowns(x_selected, y_selected):
    '''Update the dropdown options based on the selected values.'''
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
    Output('bubble-chart', 'figure'),
    [
        Input('start-date-picker', 'date'),
        Input('end-date-picker', 'date'),
        Input('metric-selector', 'value'),
        Input('x-axis-dropdown', 'value'),
        Input('y-axis-dropdown', 'value'),
        Input('breakdown', 'value'),
    ])
def update_bubble_chart(start_date, end_date, selected_metric, x_axis, y_axis, breakdown):
    '''Update the bubble chart based on the selected inputs.'''

    bubble_chart_df = bubble_chart_dataframe(
        sales_data, start_date, end_date, selected_metric, metrics_list, breakdown)

    print("This is the bubble chart dataframe:")
    print(bubble_chart_df)
    bubble_chart_fig = create_bubble_chart(
        bubble_chart_df, x_axis, y_axis, selected_metric, breakdown)

    return bubble_chart_fig
