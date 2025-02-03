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
# Calculate Growth Rates
filtered_df['Market Growth (%)'] = filtered_df['Total Market Value'].pct_change() * 100
filtered_df['ALDI Growth (%)'] = filtered_df['ALDI Total Retail Sales'].pct_change() * 100

# Apply Growth Threshold
growth_threshold = 8  # Minimum threshold for significant growth

# Apply threshold to Market Growth and ALDI Growth
filtered_df['Adjusted Market Growth (%)'] = filtered_df['Market Growth (%)'].apply(lambda x: x if abs(x) >= growth_threshold else np.nan)
filtered_df['Adjusted ALDI Growth (%)'] = filtered_df['ALDI Growth (%)'].apply(lambda x: x if abs(x) >= growth_threshold else np.nan)

# RGI Calculation
filtered_df['RGI'] = (filtered_df['Adjusted ALDI Growth (%)'] / filtered_df['Adjusted Market Growth (%)']) * 100

# SOG Calculation with Threshold
filtered_df['SOG (%)'] = ((filtered_df['ALDI Total Retail Sales'].diff()) /
                          (filtered_df['Total Market Value'].diff())) * 100
filtered_df['SOG (%)'] = filtered_df['SOG (%)'].apply(lambda x: x if abs(x) >= growth_threshold else np.nan)

# Opportunity Lost Calculation (only considering losses)
filtered_df['Expected ALDI Sales'] = filtered_df['ALDI Total Retail Sales'].shift(1) * (1 + filtered_df['Market Growth (%)'] / 100)
filtered_df['Opportunity Lost'] = filtered_df['Expected ALDI Sales'] - filtered_df['ALDI Total Retail Sales']
filtered_df['Opportunity Lost'] = filtered_df['Opportunity Lost'].apply(lambda x: x if x > 0 else np.nan)

# Layout
app.layout = html.Div([
    html.H1("ALDI Growth Dashboard"),

    dcc.Dropdown(
        id='period-filter',
        options=[{'label': str(date.date()), 'value': date} for date in filtered_df['PeriodDate']],
        multi=True,
        placeholder="Select Periods"
    ),

    dcc.Graph(id='rgi-chart'),
    dcc.Graph(id='sog-chart'),
    dcc.Graph(id='opportunity-lost-chart')
])

# Callbacks
@app.callback(
    [Output('rgi-chart', 'figure'),
     Output('sog-chart', 'figure'),
     Output('opportunity-lost-chart', 'figure')],
    [Input('period-filter', 'value')]
)
def update_charts(selected_periods):
    df = filtered_df.copy()
    if selected_periods:
        df = df[df['PeriodDate'].isin(selected_periods)]

    # RGI Chart
    fig_rgi = px.line(df, x='PeriodDate', y='RGI', title='Relative Growth Index (RGI)')
    fig_rgi.add_hline(y=100, line_dash="dash", line_color="red", annotation_text="Market Benchmark")

    # SOG Chart
    fig_sog = px.bar(df, x='PeriodDate', y='SOG (%)', title='Share of Growth (SOG)')

    # Opportunity Lost Bar Chart (only showing losses)
    colors = df['Opportunity Lost'].apply(lambda x: 'red' if pd.notnull(x) else 'gray')
    opacities = df['Opportunity Lost'].apply(lambda x: min(1, 0.3 + abs(x) / df['Opportunity Lost'].max()) if pd.notnull(x) else 0.3)

    fig_opportunity_lost = go.Figure()
    fig_opportunity_lost.add_trace(go.Bar(
        x=df['PeriodDate'], 
        y=df['Opportunity Lost'], 
        marker_color=colors,
        marker_opacity=opacities,
        name='Opportunity Lost'
    ))
    fig_opportunity_lost.update_layout(title='Opportunity Lost', xaxis_title='Period', yaxis_title='Opportunity Lost')

    return fig_rgi, fig_sog, fig_opportunity_lost

'''
