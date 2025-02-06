import plotly.express as px
import plotly.graph_objects as go

state_codes = {
    "All States": "USA",
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "District of Columbia": "DC",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",

}

list_of_state_codes = list(state_codes.values())
list_of_states = list(state_codes.keys())



'''
import pandas as pd
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Read data from pre-generated CSV files
heatmap_csv_path = 'opportunity_lost_heatmap.csv'
ranking_csv_path = 'opportunity_lost_ranking.csv'

# Load the data with multi-index
heatmap_data = pd.read_csv(heatmap_csv_path, header=[0], index_col=[0, 1, 2])  # Multi-index for category, commodity, subcommodity
date_columns = heatmap_data.columns[:-1]  # Exclude 'Total' column
ranking_table = pd.read_csv(ranking_csv_path)

# Yearly Opportunity Lost List
# Extract year from date columns
years = [col[:4] for col in date_columns if col[:4].isdigit()]

# Sum Opportunity Lost for each year
yearly_opportunity_loss = heatmap_data[years].sum().reset_index()
yearly_opportunity_loss.columns = ['Year', 'Opportunity Lost']

# Simplify Y-axis labels to avoid redundancy
def simplify_labels(index):
    cat, com, sub = index
    if cat == com == sub:
        return f"{sub}"
    elif com == sub:
        return f"{cat} - {sub}"
    else:
        return f"{cat} - {com} - {sub}"

# Dash App Setup
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("ALDI Opportunity Lost Dashboard", className="text-center text-primary mb-4"), width=12)
    ]),

    # Heatmap
    dbc.Row([
        dbc.Col(dcc.Graph(
            id='opportunity-lost-heatmap',
            figure=go.Figure(data=go.Heatmap(
                z=heatmap_data[date_columns].values,
                x=date_columns,
                y=[simplify_labels(index) for index in heatmap_data.index],
                colorscale='Reds',
                colorbar_title='Opportunity Lost'
            ))
        ), width=12)
    ]),

    # Yearly Opportunity Lost List
    dbc.Row([
        dbc.Col([
            html.H2("Yearly Opportunity Loss", className="text-center"),
            dash_table.DataTable(
                data=yearly_opportunity_loss.to_dict('records'),
                columns=[{"name": col, "id": col} for col in yearly_opportunity_loss.columns],
                style_table={'margin': '20px 0'},
                style_cell={'textAlign': 'center'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
            )
        ], width=12)
    ]),

    # Ranking Table
    dbc.Row([
        dbc.Col([
            html.H2("2024 Opportunity Lost Ranking", className="text-center"),
            dash_table.DataTable(
                data=ranking_table.to_dict('records'),
                columns=[{"name": col, "id": col} for col in ranking_table.columns],
                style_table={'margin': '20px 0'},
                style_cell={'textAlign': 'center'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
            )
        ], width=12)
    ])
], fluid=True)

if __name__ == '__main__':
    app.run_server(debug=True)

print(f"Opportunity Lost Heatmap loaded from {heatmap_csv_path}")
print(f"Opportunity Lost Ranking Table loaded from {ranking_csv_path}")



'''
