import pandas as pd  # (version 1.0.0)
import plotly  # (version 4.5.4) pip install plotly==4.5.4
import plotly.express as px
import dash  # (version 1.9.1) pip install dash==1.9.1
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


from index import app
from Functions.data_loader import load_and_preprocess_data
from Functions.USA_map import state_codes
from Functions.home_page_functions import metric_dropdown, update_kpi_title, update_map_title, update_metric_trends_title, selected_year_previous_year_data_of_state, aggregate_data_by_month, create_line_chart, aggregate_kpi_level, create_indicator, choropleth_dataframe, choropleth_map_creation

# File path to the Excel file
file_path = 'assets/Sample - Superstore.xlsx'
# Load and preprocess the data
sales_data, unique_years = load_and_preprocess_data(
    file_path)

home_page_layout = html.Div([

    dbc.Row([

        dbc.Col([
            dbc.Row([
                html.H4(id='map-title',
                    children="Overview by State", className='title'),
            ]),

            dbc.Row([
                dbc.Col(html.Div([dcc.Graph(
                    id='choropleth-map', config={'displayModeBar': False})], className='map-container'), width=12),
            ], className='map-row'),

            dbc.Row([
                    dbc.Col(html.H4(id='summary-title',
                                    children="SuperStore Executive Summary"), className='title', width=12)
                    ]),

            dbc.Row([
                    dbc.Col(html.Div([dcc.Graph(id='sales-kpi', config={'displayModeBar': False})],
                                     className='graph-container'), width=3),
                    dbc.Col(html.Div([dcc.Graph(id='quantity-kpi', config={'displayModeBar': False})],
                                     className='graph-container'), width=3),
                    dbc.Col(html.Div([dcc.Graph(id='profit-kpi', config={'displayModeBar': False})],
                                     className='graph-container'), width=3),
                    dbc.Col(html.Div([dcc.Graph(id='margin-kpi', config={'displayModeBar': False}),],
                                     className='graph-container',), width=3),
                    ], className='graph-row'),

            dbc.Row([
                html.H4(id='trend-graph-title',
                    children="Metric trends", className='title'),
            ]),

            dbc.Row([
                    dbc.Col(html.Div([dcc.Graph(id='sales-chart', config={'displayModeBar': False}, style={
                        'height': '260px'})], className='graph-container'), width=3),
                    dbc.Col(html.Div([dcc.Graph(id='quantity-chart', config={'displayModeBar': False}, style={
                        'height': '260px'})], className='graph-container'), width=3),
                    dbc.Col(html.Div([dcc.Graph(id='profit-chart', config={'displayModeBar': False}, style={
                        'height': '260px'})], className='graph-container'), width=3),
                    dbc.Col(html.Div([dcc.Graph(id='margin-chart', config={'displayModeBar': False}, style={
                        'height': '260px'})], className='graph-container'), width=3),
                    ], className='graph-row'),

        ], className='dashboard-column', width=10),

        dbc.Col([
            html.H4("Controls", className="text-center"),
            html.Label("Select Year", className="dropdown-label"),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': str(year), 'value': year}
                         for year in unique_years],
                value=max(unique_years),
                clearable=False,
                className='dropdown-style'
            ),
            html.Label("Select Metric", className="dropdown-label"),
            dcc.Dropdown(
                id='metric-dropdown',
                options=metric_dropdown,
                value='Profit',
                clearable=False,
                className='dropdown-style'
            ),
            html.Label("Select State", className="dropdown-label"),
            dcc.Dropdown(
                id='state-dropdown',
                options=[{'label': state, 'value': code}
                         for state, code in state_codes.items()],
                value=next(iter(state_codes.values())),
                clearable=False,
                className='dropdown-style'
            ),
        ], className='control-column', width=2)
    ])
])


@app.callback(
    [Output('map-title', 'children'),
     Output('choropleth-map', 'figure'),
     Output('summary-title', 'children'),
     Output('sales-kpi', 'figure'),
     Output('quantity-kpi', 'figure'),
     Output('profit-kpi', 'figure'),
     Output('margin-kpi', 'figure'),
     Output('trend-graph-title', 'children'),
     Output('sales-chart', 'figure'),
     Output('quantity-chart', 'figure'),
     Output('profit-chart', 'figure'),
     Output('margin-chart', 'figure')
     ],
    [Input('year-dropdown', 'value'),
     Input('metric-dropdown', 'value'),
     Input('state-dropdown', 'value'),
     ]

)
def display_selected(year, metric, state_code):
    '''Display the selected data based on the filters. This will generate the map, KPIs, and trend graphs.'''

    print(f'Year: {year}, State: {state_code}')
    print(f'Type of year: {type(year)}, Type of state: {type(state_code)}')

    current_data, previous_data = selected_year_previous_year_data_of_state(
        sales_data, year, state_code, unique_years)

    # Aggregate data by month for the trend graphs
    aggregated_current = aggregate_data_by_month(current_data)
    aggregated_previous = aggregate_data_by_month(
        previous_data) if previous_data is not None else None

    # Title updates
    map_title = update_map_title(year, metric)
    kpi_title = update_kpi_title(year, state_code)
    trend_graph_title = update_metric_trends_title(year, state_code)

    # Create charts
    sales_chart = create_line_chart(
        aggregated_current, aggregated_previous, 'Sales')
    quantity_chart = create_line_chart(
        aggregated_current, aggregated_previous, 'Quantity')
    profit_chart = create_line_chart(
        aggregated_current, aggregated_previous, 'Profit', )
    margin_chart = create_line_chart(
        aggregated_current, aggregated_previous, 'Profit Margin')

    print(f'Current data:\n{aggregated_current}')
    print("********************************")
    print(f'Previous data:\n {aggregated_previous}')

    # Aggregate KPI data
    aggregated_kpi_data = aggregate_kpi_level(sales_data, state_code,)
    kpi_display_data = aggregated_kpi_data[aggregated_kpi_data['Year'] == year]

    print(f'KPI data:\n{aggregated_kpi_data}')
    print(kpi_display_data)

    sales_kpi = create_indicator(kpi_display_data['Sales'].iloc[0],
                                 kpi_display_data['Sales Change'].iloc[0], 'Sales', is_currency=True, is_percentage=False)

    quantity_kpi = create_indicator(kpi_display_data['Quantity'].iloc[0],
                                    kpi_display_data['Quantity Change'].iloc[0], 'Quantity', is_currency=False, is_percentage=False)

    profit_kpi = create_indicator(kpi_display_data['Profit'].iloc[0],
                                  kpi_display_data['Profit Change'].iloc[0], 'Profit', is_currency=True, is_percentage=False)

    margin_kpi = create_indicator(kpi_display_data['Profit Margin'].iloc[0],
                                  kpi_display_data['Profit Margin Change'].iloc[0], 'Profit Margin', is_currency=False, is_percentage=True)

    # Create choropleth map
    choropleth_data = choropleth_dataframe(sales_data, year)

    print(f'Choropleth data:\n{choropleth_data}')

    choropleth_fig = choropleth_map_creation(choropleth_data, metric, year)

    return map_title, choropleth_fig, kpi_title, sales_kpi, quantity_kpi, profit_kpi, margin_kpi, trend_graph_title, sales_chart, quantity_chart, profit_chart, margin_chart
