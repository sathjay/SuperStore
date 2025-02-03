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

# RGI Calculation
filtered_df['RGI'] = (filtered_df['ALDI Growth (%)'] / filtered_df['Market Growth (%)']) * 100

# SOG Calculation
filtered_df['SOG (%)'] = ((filtered_df['ALDI Total Retail Sales'].diff()) /
                          (filtered_df['Total Market Value'].diff())) * 100

# Opportunity Gained or Lost Calculation
# Calculated as the difference between expected ALDI sales (if growth matched the market) and actual ALDI sales
filtered_df['Expected ALDI Sales'] = filtered_df['ALDI Total Retail Sales'].shift(1) * (1 + filtered_df['Market Growth (%)'] / 100)
filtered_df['Opportunity Gained or Lost'] = filtered_df['Expected ALDI Sales'] - filtered_df['ALDI Total Retail Sales']


dcc.Graph(id='rgi-chart'),
    dcc.Graph(id='sog-chart'),
    dcc.Graph(id='opportunity-gained-lost-chart')

    # RGI Chart
    fig_rgi = px.line(df, x='PeriodDate', y='RGI', title='Relative Growth Index (RGI)')
    fig_rgi.add_hline(y=100, line_dash="dash", line_color="red", annotation_text="Market Benchmark")

    # SOG Chart
    fig_sog = px.bar(df, x='PeriodDate', y='SOG (%)', title='Share of Growth (SOG)')

    # Opportunity Gained or Lost Bar Chart
    colors = df['Opportunity Gained or Lost'].apply(lambda x: 'blue' if x > 0 else 'red')
    opacities = df['Opportunity Gained or Lost'].apply(lambda x: min(1, 0.3 + abs(x) / df['Opportunity Gained or Lost'].max()))

    fig_opportunity_gained_lost = go.Figure()
    fig_opportunity_gained_lost.add_trace(go.Bar(
        x=df['PeriodDate'], 
        y=df['Opportunity Gained or Lost'], 
        marker_color=colors,
        marker_opacity=opacities,
        name='Opportunity Gained or Lost'
    ))
    fig_opportunity_gained_lost.update_layout(title='Opportunity Gained or Lost', xaxis_title='Period', yaxis_title='Opportunity Gained or Lost')

    return fig_rgi, fig_sog, fig_opportunity_gained_lost

'''
