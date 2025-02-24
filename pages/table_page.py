import pandas as pd  # (version 1.0.0)
import plotly  # (version 4.5.4) pip install plotly==4.5.4
import plotly.express as px
import dash  # (version 1.9.1) pip install dash==1.9.1
from dash import dcc, no_update, html, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from index import app

from index import app
from Functions.data_loader import load_and_preprocess_data, add_week_and_quarter_for_table_page
from Functions.table_page_functions import create_query, filter_dataframe, validation_and_display_message

# File path to the Excel file
file_path = 'assets/Sample - Superstore.xlsx'
# Load and preprocess the data
sales_data, unique_years = load_and_preprocess_data(
    file_path)
# Add 'Week' and 'Quarter' columns. Columns are remaned here for df.query() to work
sales_data_with_q_info = add_week_and_quarter_for_table_page(sales_data)


table_page_layout = html.Div([

    dbc.Row([html.P('SuperStore Data Table:', className='table-heading')],
            className='table-heading-row'),

    dbc.Row([

        dbc.Col([
                dash_table.DataTable(
                    id='table',
                    style_table={'overflowX': 'auto'},
                    page_size=20,  # Number of rows per page
                    # Ensures cells are wide enough to show content
                    style_cell={'minWidth': '80px',
                                'width': '100px', 'maxWidth': '200px'},
                    filter_action='native',  # Optional: enable filtering by column
                    sort_action='native',  # Optional: enable sorting
                    sort_mode='multi',  # Allow sorting on multiple columns
                    page_action='native',  # Enable pagination

                    fixed_rows={'headers': True},
                    style_data={
                        'color': 'black',
                        'backgroundColor': 'white',
                        'fontSize': '12.5px',
                    },
                    style_header={'backgroundColor': 'blue',
                                  'color': 'white',
                                  'fontSize': '14px',
                                  'whiteSpace': 'normal',
                                  'height': 'auto',
                                  },
                )

                ], className='table-display', width=10),

        dbc.Col([
            dbc.Row([
                html.P('Table Filter:',
                       className='table-filter-heading'),
                dbc.Row([dbc.Row([
                    html.Label(
                        'Segment:', className='table-input-label')
                ]),
                    dbc.Row([
                        dcc.Dropdown(
                            id='filter-dropdown-1',
                            options=[{'label': segment, 'value': segment}
                                     for segment in sales_data_with_q_info['Segment'].unique()],
                            value='Consumer',
                            placeholder="Select a Segment"
                        ),
                    ])
                ], className='table-filter-container'),

                dbc.Row([dbc.Row([
                    html.Label(
                        'Category:', className='table-input-label')
                ]),
                    dbc.Row([
                        dcc.Dropdown(
                            id='filter-dropdown-2',
                            options=[{'label': category, 'value': category}
                                     for category in sales_data_with_q_info['Category'].unique()],
                            value='Technology',
                            placeholder="Select a Category"
                        ),
                    ])
                ], className='table-filter-container'),



                dbc.Row([dbc.Row([
                    html.Label(
                        'Sub-Category:', className='table-input-label')
                ]),
                    dbc.Row([
                        dcc.Dropdown(
                            id='filter-dropdown-3',
                            options=[{'label': sub_category, 'value': sub_category}
                                     for sub_category in sales_data_with_q_info['SubCategory'].unique()],
                            value='Phones',
                            placeholder="Select a Sub-Category"
                        ),
                    ])

                ], className='table-filter-container'),

            ], className='table-filter-row'),

            dbc.Row([

                html.P('Filter by Geography:',
                       className='table-filter-heading'),

                dbc.Row([dbc.Row([
                    html.Label('Region:', className='table-input-label')
                ]),
                    dbc.Row([
                        dcc.Dropdown(
                            id='region-dropdown',
                            options=[{'label': region, 'value': region}
                                     for region in sales_data_with_q_info['Region'].unique()],
                            value=None,
                            placeholder="Select a Region"
                        ),
                    ])
                ], className='table-filter-container'),

                dbc.Row([dbc.Row([
                    html.Label('State:', className='table-input-label')
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
                            'City:', className='table-input-label')
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

    ], className='table-container'),

    dbc.Row([html.P('Data Entry Section:', className='data-entry-heading')]),

    dbc.Row([
        dbc.Col([
            html.P('Order ID:', className='input-label'),
            dbc.Input(id='input-order-id',
                      placeholder='Enter Order ID', type='text', className='input-field-class'),
            html.P('Note: New Order ID entered must be unique.',
                   className='input-note')
        ], className='input-field-container', width=2),

        dbc.Col([
            html.P('Customer Name:', className='input-label'),
            dbc.Input(id='input-customer-name',
                      placeholder='Enter Customer Name', type='text', className='input-field-class'),

        ], className='input-field-container', width=2),
        dbc.Col([
            html.P('Product Name:', className='input-label'),
            dbc.Input(id='input-product',
                      placeholder='Enter Product Name', type='text', className='input-field-class'),
        ], className='input-field-container', width=2),

        dbc.Col([
            html.P('Quantity:', className='input-label'),
            dbc.Input(id='input-quantity',
                      placeholder='Enter Quantity', type='text', className='input-field-class'),
        ], className='input-field-container', width=2),

        dbc.Col([
            html.P('Price:', className='input-label'),
            dbc.Input(id='input-price',
                      placeholder='Enter Price', type='text', className='input-field-class'),
        ], className='input-field-container', width=2),

        dbc.Col([
            dbc.Button('Add Data', id='add-data-button',
                       color='primary', className='add-data-button'),
        ], className='button-container', width=2),
    ], className='data-entry-row'),

    dbc.Row([
        html.Div([
            html.P(id='feedback-message', style={'color': 'red', 'margin': '10px'})])
    ], className='data-entry-message-container')
])


@ app.callback(
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
    '''Update the dropdown options based on the selected region and state.'''
    if selected_region == None:
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


@ app.callback(
    [Output('table', 'data'),
     Output('table', 'columns')],
    [Input('filter-dropdown-1', 'value'),
     Input('filter-dropdown-2', 'value'),
     Input('filter-dropdown-3', 'value'),
     Input('region-dropdown', 'value'),
     Input('state-dropdown', 'value'),
        Input('city-dropdown', 'value')],
)
def update_table(selected_segment, selected_category, selected_sub_category, selected_region, selected_state, selected_city):
    '''Update the table based on the selected filters.'''

    print('Segment: {}, \nCategory: {}, \nSubCategory: {}, \nState: {}, \nRegion: {}, \nCity: {}'.format(
        selected_segment, selected_category, selected_sub_category, selected_region, selected_state, selected_city))

    query = ''  # Initialize query string
    query = create_query(selected_segment, selected_category,
                         selected_sub_category, selected_region, selected_state, selected_city)

    print(f'Query: {query}')

    filtered_df = pd.DataFrame()  # Initialize an empty DataFrame
    filtered_df = filter_dataframe(sales_data_with_q_info, query)

    print(f'Filtered Data: {filtered_df.head()}')

    data = filtered_df.to_dict('records')
    columns = [{"name": i, "id": i} for i in filtered_df.columns]

    return data, columns


@app.callback(
    Output('feedback-message', 'children'),
    Input('add-data-button', 'n_clicks'),
    [State('input-order-id', 'value'),
     State('input-customer-name', 'value'),
     State('input-product', 'value'),
     State('input-quantity', 'value'),
     State('input-price', 'value')],
    prevent_initial_call=True)
def table_data_entry(n_clicks, order_id, customer_name, product, quantity, price):
    '''Add new data to the table based on the input fields.'''
    print('Order ID: {}, Customer Name: {}, Product: {}, Quantity: {}, Price: {}'.format(
        order_id, customer_name, product, quantity, price))

    global sales_data_with_q_info

    ui_message, data_insert_flag = validation_and_display_message(
        sales_data_with_q_info, order_id, customer_name, product, quantity, price)

    if data_insert_flag == True:

        new_row = {'Order ID': order_id, 'Customer Name': customer_name, 'Product': product,
                   'Quantity': quantity, 'Price': price}

        # Append to the dataframe
        # Convert new row into a DataFrame to append
        new_df = pd.DataFrame([new_row])
        sales_data_with_q_info = pd.concat(
            [sales_data_with_q_info, new_df], ignore_index=True)

        return ui_message

    return ui_message
'''
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash import dcc
from dash.dependencies import Input, Output
from components.sidebar import sidebar  # Import sidebar component

# Initialize Dash app
app = dash.Dash(
    external_stylesheets=[
        dbc.icons.FONT_AWESOME,
        dbc.icons.BOOTSTRAP,
        dbc.themes.BOOTSTRAP,
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css'
    ],
    assets_folder='assets',
    use_pages=True,
    pages_folder='pages',
    suppress_callback_exceptions=True
)

# Define layout
app.layout = html.Div([
    sidebar,  # Sidebar imported from components
    # Page content container
    html.Div([dash.page_container], className='page_content')
], className='full_page')

# Run app
if __name__ == "__main__":
    app.run_server(debug=True)



import dash_bootstrap_components as dbc
import dash_html_components as html

# Define icons and URLs
tabs = [
    {"icon": "fas fa-home fa-lg", "label": "Home", "href": "/"},
    {"icon": "fas fa-database fa-lg", "label": "NielsenIQ Data", "href": "/nielseniq"},
    {"icon": "fas fa-sort-amount-down fa-lg",
        "label": "Category Ranking", "href": "/category-ranking"},
    {"icon": "fas fa-tags fa-lg", "label": "Brand Ranking", "href": "/brand-ranking"},
    {"icon": "fas fa-box-open fa-lg",
        "label": "Product Ranking", "href": "/product-ranking"},
    {"icon": "fas fa-coins fa-lg", "label": "Financial Projection",
        "href": "/financial-projection"}
]

# Sidebar layout
sidebar = html.Div([
    # Placeholder for ALDI Internal Division Logo
    html.Div("ALDI Internal Logo", className='logo-placeholder'),

    # App Name
    html.H4("Private Label vs Brands", className="app-title"),

    # Navigation Menu
    dbc.Nav([
        dbc.NavLink(
            dbc.Row([
                dbc.Col(html.I(className=tab["icon"]),
                        width=3, className='nav-icon'),
                dbc.Col(tab["label"], width=9, className='nav-text')
            ], align='center', className='nav-row'),
            href=tab["href"], active="exact"
        ) for tab in tabs
    ], vertical=True, pills=True, className="nav-menu"),

    # Placeholder for ALDI Corporate Logo
    html.Div("ALDI Corporate Logo", className='logo-placeholder-bottom')
], className='sidebar')


/* Full page layout */
.full_page {
  display: flex;
  height: 100vh;
  width: 100vw;
  margin: 0;
  padding: 0;
}

/* Sidebar styling */
.sidebar {
  width: 8%;
  height: 100vh;
  background-color: #e9ecef; /* Light grey */
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 0px;
  position: fixed;
  left: 0;
  top: 0;
}

/* Placeholder logos */
.logo-placeholder,
.logo-placeholder-bottom {
  width: 100%;
  height: 80px;
  background-color: #d6d6d6; /* Placeholder color */
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: #333;
  margin-bottom: 10px;
}

/* App title styling */
.app-title {
  font-size: 14px;
  text-align: center;
  font-weight: bold;
  padding: 10px 0;
}

/* Navigation menu */
.nav-menu {
  flex-grow: 1;
  width: 100%;
}

.nav-menu a {
  text-align: left;
  font-size: 13px;
  color: #333;
  padding: 10px;
  text-decoration: none;
  display: block;
}

.nav-menu a:hover {
  background-color: #9eb4cc;
  color: white;
}
/* Navigation icon styling */
.nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Navigation text styling */
.nav-text {
  display: flex;
  align-items: center;
}

/* Main content */
.page_content {
  margin-left: 9%;
  width: 92%;
  padding: 10px;
  overflow-y: auto;
}

