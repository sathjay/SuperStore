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
yearly_summary_csv_path = 'yearly_opportunity_summary.csv'

# Load the data with multi-index
heatmap_data = pd.read_csv(heatmap_csv_path, header=[0], index_col=[0, 1, 2])  # Multi-index for category, commodity, subcommodity
date_columns = heatmap_data.columns[:-1]  # Exclude 'Total' column
ranking_table = pd.read_csv(ranking_csv_path)
yearly_opportunity_loss = pd.read_csv(yearly_summary_csv_path)

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
print(f"Yearly Opportunity Summary loaded from {yearly_summary_csv_path}")







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

import pandas as pd
import numpy as np

# Read the CSV file
file_path = 'aldi_scg_grouped_df.csv'  # Ensure this file is in the same directory
aldi_df = pd.read_csv(file_path)

# Ensure correct datetime format
aldi_df['PeriodDate'] = pd.to_datetime(aldi_df['PeriodDate'], format='%Y-%m-%d')

# Sort by category_nm, commodity_group_nm, subcommodity_group_nm, and PeriodDate
aldi_df = aldi_df.sort_values(by=['category_nm', 'commodity_group_nm', 'subcommodity_group_nm', 'PeriodDate'])

# Calculate Market Growth Rate
aldi_df['Market Growth Rate'] = aldi_df.groupby('subcommodity_group_nm')['Total Market Value'].pct_change()

# Calculate Expected ALDI Sales
aldi_df['Expected ALDI Sales'] = aldi_df.groupby('subcommodity_group_nm')['sales_value ALDI'].shift(1) * (1 + aldi_df['Market Growth Rate'])

# Calculate Opportunity Lost
aldi_df['Opportunity Lost'] = aldi_df['Expected ALDI Sales'] - aldi_df['sales_value ALDI']
aldi_df['Opportunity Lost'] = aldi_df['Opportunity Lost'].apply(lambda x: x if x > 0 else 0)

# Pivot table for Heatmap
heatmap_data = aldi_df.pivot_table(
    index=['category_nm','commodity_group_nm','subcommodity_group_nm'],
    columns=aldi_df['PeriodDate'].dt.to_period('M').astype(str),
    values='Opportunity Lost',
    aggfunc='sum',
    fill_value=0
)

# Add totals
heatmap_data['Total'] = heatmap_data.sum(axis=1)
heatmap_data.loc['Total'] = heatmap_data.sum(axis=0)

#Round values to Zero Decimal
heatmap_data = heatmap_data.round(0)

# Save Heatmap Data as CSV
heatmap_csv_path = 'opportunity_lost_heatmap.csv'
heatmap_data.to_csv(heatmap_csv_path)

# Filter data for the year 2024
aldi_2024_df = aldi_df[aldi_df['PeriodDate'].dt.year == 2024]

# Create Ranking Table based on Opportunity Lost in 2024
ranking_table = aldi_2024_df.groupby('subcommodity_group_nm')['Opportunity Lost'].sum().reset_index()
ranking_table = ranking_table.sort_values(by='Opportunity Lost', ascending=False)

# Save Ranking Table as CSV
ranking_csv_path = 'opportunity_lost_ranking.csv'
ranking_table.to_csv(ranking_csv_path, index=False)

print(f"Opportunity Lost Heatmap saved to {heatmap_csv_path}")
print(f"Opportunity Lost Ranking Table saved to {ranking_csv_path}")


import pandas as pd
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Read the CSV file
file_path = 'aldi_scg_grouped_df.csv'  # Ensure this file is in the same directory
aldi_df = pd.read_csv(file_path)

# Ensure correct datetime format
aldi_df['PeriodDate'] = pd.to_datetime(aldi_df['PeriodDate'], format='%Y-%m-%d')

# Sort by category_nm, commodity_group_nm, subcommodity_group_nm, and PeriodDate
aldi_df = aldi_df.sort_values(by=['category_nm', 'commodity_group_nm', 'subcommodity_group_nm', 'PeriodDate'])

# Calculate Market Growth Rate
aldi_df['Market Growth Rate'] = aldi_df.groupby('subcommodity_group_nm')['Total Market Value'].pct_change()

# Calculate Expected ALDI Sales
aldi_df['Expected ALDI Sales'] = aldi_df.groupby('subcommodity_group_nm')['sales_value ALDI'].shift(1) * (1 + aldi_df['Market Growth Rate'])

# Calculate Opportunity Lost
aldi_df['Opportunity Lost'] = aldi_df['Expected ALDI Sales'] - aldi_df['sales_value ALDI']
aldi_df['Opportunity Lost'] = aldi_df['Opportunity Lost'].apply(lambda x: x if x > 0 else 0)

# Pivot table for Heatmap
heatmap_data = aldi_df.pivot_table(
    index=['category_nm','commodity_group_nm','subcommodity_group_nm'],
    columns=aldi_df['PeriodDate'].dt.to_period('M').astype(str),
    values='Opportunity Lost',
    aggfunc='sum',
    fill_value=0
)

# Add totals
heatmap_data['Total'] = heatmap_data.sum(axis=1)
heatmap_data.loc['Total'] = heatmap_data.sum(axis=0)

# Round values to Zero Decimal
heatmap_data = heatmap_data.round(0)

# Save Heatmap Data as CSV
heatmap_csv_path = 'opportunity_lost_heatmap.csv'
heatmap_data.to_csv(heatmap_csv_path)

# Filter data for the year 2024
aldi_2024_df = aldi_df[aldi_df['PeriodDate'].dt.year == 2024]

# Create Ranking Table based on Opportunity Lost in 2024
ranking_table = aldi_2024_df.groupby('subcommodity_group_nm')['Opportunity Lost'].sum().reset_index()
ranking_table = ranking_table.sort_values(by='Opportunity Lost', ascending=False)

# Save Ranking Table as CSV
ranking_csv_path = 'opportunity_lost_ranking.csv'
ranking_table.to_csv(ranking_csv_path, index=False)

# Create Yearly Opportunity Summary
yearly_opportunity_summary = aldi_df.groupby(aldi_df['PeriodDate'].dt.year)['Opportunity Lost'].sum().reset_index()
yearly_opportunity_summary.columns = ['Year', 'Opportunity Lost']

# Save Yearly Opportunity Summary as CSV
yearly_summary_csv_path = 'yearly_opportunity_summary.csv'
yearly_opportunity_summary.to_csv(yearly_summary_csv_path, index=False)

print(f"Opportunity Lost Heatmap saved to {heatmap_csv_path}")
print(f"Opportunity Lost Ranking Table saved to {ranking_csv_path}")
print(f"Yearly Opportunity Summary saved to {yearly_summary_csv_path}")




'''
