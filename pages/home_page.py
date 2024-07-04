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
from Functions.data_loader import load_and_preprocess_data
from Functions.USA_map import state_codes
from Functions.home_page_functions import selected_year_previous_year_data_of_state, aggregate_data_by_month, create_line_chart, aggregate_kpi_level, create_indicator


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

            dbc.Row([
                dbc.Col(html.Div([dcc.Graph(id='sales-kpi')],
                                 className='graph-container'), width=3),
                dbc.Col(html.Div([dcc.Graph(id='quantity-kpi')],
                                 className='graph-container'), width=3),
                dbc.Col(html.Div([dcc.Graph(id='profit-kpi')],
                                 className='graph-container'), width=3),
                dbc.Col(html.Div([dcc.Graph(id='margin-kpi')],
                                 className='graph-container'), width=3),
            ], className='graph-row'),




            dbc.Row([
                dbc.Col(html.Div([
                    dcc.Graph(id='sales-chart',
                              config={'displayModeBar': False}, style={'height': '260px'})
                ], className='graph-container'), width=3),

                dbc.Col(html.Div([
                    dcc.Graph(id='quantity-chart',
                              config={'displayModeBar': False}, style={'height': '260px'})
                ], className='graph-container'), width=3),

                dbc.Col(html.Div([
                    dcc.Graph(id='profit-chart',
                              config={'displayModeBar': False}, style={'height': '260px'})
                ], className='graph-container'), width=3),

                dbc.Col(html.Div([
                    dcc.Graph(id='margin-chart',
                              config={'displayModeBar': False}, style={'height': '260px'})
                ], className='graph-container'), width=3),
            ], className='graph-row')

        ]), width=10),

        dbc.Col(html.Div([
            html.H4("Controls", className="text-center"),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': str(year), 'value': year}
                         for year in unique_years],
                value=max(unique_years),
                style={'width': '100%', 'padding': '10px'}
            ),
            dcc.Dropdown(
                id='state-dropdown',
                # Assuming state_codes is already defined or imported
                options=[{'label': state, 'value': code}
                         for state, code in state_codes.items()],
                value=next(iter(state_codes.values())),
                style={'width': '100%', 'padding': '10px'}
            ),
            html.Div(id='display-selected-state')
        ]), width=2),
    ])
])


@app.callback(
    [Output('sales-kpi', 'figure'),
     Output('quantity-kpi', 'figure'),
     Output('profit-kpi', 'figure'),
     Output('margin-kpi', 'figure'),
     Output('sales-chart', 'figure'),
     Output('quantity-chart', 'figure'),
     Output('profit-chart', 'figure'),
     Output('margin-chart', 'figure')],
    [Input('year-dropdown', 'value'),
     Input('state-dropdown', 'value')]

)
def display_selected(year, state_code):

    print(f'Year: {year}, State: {state_code}')
    print(f'Type of year: {type(year)}, Type of state: {type(state_code)}')

    current_data, previous_data = selected_year_previous_year_data_of_state(
        sales_data, year, state_code, unique_years)

    aggregated_current = aggregate_data_by_month(current_data)
    aggregated_previous = aggregate_data_by_month(
        previous_data) if previous_data is not None else None

    print(aggregated_current)
    print('******')
    print(aggregated_previous)

    # Create charts
    sales_chart = create_line_chart(
        aggregated_current, aggregated_previous, 'Sales')
    quantity_chart = create_line_chart(
        aggregated_current, aggregated_previous, 'Quantity')
    profit_chart = create_line_chart(
        aggregated_current, aggregated_previous, 'Profit', )
    margin_chart = create_line_chart(
        aggregated_current, aggregated_previous, 'Profit Margin')

    aggregated_kpi_data = aggregate_kpi_level(sales_data, state_code,)
    kpi_display_data = aggregated_kpi_data[aggregated_kpi_data['Year'] == year]

    print(kpi_display_data)

    sales_kpi = create_indicator(kpi_display_data['Sales'].iloc[0],
                                 kpi_display_data['Sales Change'].iloc[0], 'Sales', is_currency=True, is_percentage=False)

    quantity_kpi = create_indicator(kpi_display_data['Quantity'].iloc[0],
                                    kpi_display_data['Quantity Change'].iloc[0], 'Quantity', is_currency=False, is_percentage=False)

    profit_kpi = create_indicator(kpi_display_data['Profit'].iloc[0],
                                  kpi_display_data['Profit Change'].iloc[0], 'Profit', is_currency=True, is_percentage=False)

    margin_kpi = create_indicator(kpi_display_data['Profit Margin'].iloc[0],
                                  kpi_display_data['Profit Margin Change'].iloc[0], 'Profit Margin', is_currency=False, is_percentage=True)

    return sales_kpi, quantity_kpi, profit_kpi, margin_kpi, sales_chart, quantity_chart, profit_chart, margin_chart
