import pandas as pd
import plotly.express as px
import calendar
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def selected_year_previous_year_data_of_state(df, selected_year, selected_state, unique_years):
    # Filter data for the selected year
    selected_year = int(selected_year)

    current_selected_year_data = df[df['Year'] == selected_year]

    # Initialize previous year data as None
    previous_year_selected_data = None

    # Check if the selected year is not the lowest year
    if selected_year > min(unique_years):
        previous_year_selected_data = df[df['Year'] == selected_year - 1]

    # Filter data for the selected state if it is not 'All' (USA)
    if selected_state != "USA":
        current_selected_year_data = current_selected_year_data[
            current_selected_year_data['State Code'] == selected_state]
        if previous_year_selected_data is not None:
            previous_year_selected_data = previous_year_selected_data[
                previous_year_selected_data['State Code'] == selected_state]

    return current_selected_year_data, previous_year_selected_data


def aggregate_data_by_month(df):
    if df.empty:
        return pd.DataFrame()  # Return an empty DataFrame if the input is empty

    # Ensure 'Year' and 'Month' are included in the columns to keep
    columns_to_keep = ['Year', 'Month', 'Sales', 'Quantity', 'Profit']
    df = df[columns_to_keep]

    # Convert month numbers to month names using the calendar module
    df['Month'] = df['Month'].apply(lambda x: calendar.month_abbr[x])

    # Group by 'Year' and 'Month' and aggregate Sales, Quantity, and Profit
    aggregated_data = df.groupby(['Year', 'Month']).agg({
        'Sales': 'sum',
        'Quantity': 'sum',
        'Profit': 'sum'
    }).reset_index()

    # Calculate profit margin as a percentage
    aggregated_data['Profit Margin'] = (
        aggregated_data['Profit'] / aggregated_data['Sales'] * 100).round(2)

    # Sorting by 'Year' and 'Month' to ensure the output is in chronological order
    # Ensure sorting takes the actual month sequence into account if necessary
    month_to_num = {name: num for num,
                    name in enumerate(calendar.month_abbr) if name}
    aggregated_data['Month'] = pd.Categorical(aggregated_data['Month'],
                                              categories=list(
                                                  calendar.month_abbr[1:]),
                                              ordered=True)
    aggregated_data.sort_values(by=['Year', 'Month'], inplace=True)

    return aggregated_data


def create_line_chart(current_data, previous_data, metric):

    # Check if previous data is available and merge with current data if it is
    if previous_data is not None:
        # Concatenate current and previous year data without changing the 'Year' values
        data = pd.concat([current_data, previous_data])
    else:
        # Use current data only if no previous data
        data = current_data

    # Custom color map for clarity and aesthetics
    # Assuming 'Year' columns in current and previous data are already in the format like "2021", "2020"
    color_discrete_map = {current_data['Year'].iloc[0]: 'darkblue',
                          previous_data['Year'].iloc[0] if previous_data is not None else None: 'lightgrey'}

    # Plot using Plotly Express
    fig = px.line(data, x='Month', y=metric, color='Year',
                  title=metric,
                  labels={'Month': '', metric: ''},
                  color_discrete_map=color_discrete_map,
                  hover_data={'Year': True, metric: ':.2f', 'Month': True})

    # Update layout for the chart
    fig.update_layout(
        plot_bgcolor='white',  # Background color
        paper_bgcolor='white',  # Background color around the chart
        showlegend=False,  # Turn off the legend

        margin=dict(l=0, r=0, t=20, b=0),
        yaxis=dict(
            showline=True,  # Show y-axis line
            showgrid=False,  # Hide grid lines
            linecolor='black',  # y-axis line color
            zeroline=False,  # Remove the zero line for a cleaner look
            side='left'  # Ensure y-axis is on the left
        ),
        xaxis=dict(
            showline=True,  # Show x-axis line
            showgrid=False,  # Hide grid lines
            linecolor='black',  # x-axis line color

            tickmode='array',

            # Specify months to show: January, April, July, October
            tickvals=[1, 4, 7, 10],
            ticktext=['Jan', 'Apr', 'Jul', 'Oct'],
            range=[.9, 12.1]  # Adjust the range to start the x-axis at Jan
        ),
        title={
            'text': metric,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},

        titlefont={'size': 15},

        hoverlabel=dict(
            bgcolor="lightyellow",  # Set background color to light yellow
            font_size=12,  # Optional: adjust font size
            font_family="Roboto"  # Optional: adjust font family
        ),
    )

    # Add markers to the line plot
    fig.update_traces(mode='lines+markers',
                      marker=dict(color='grey', size=7),
                      hovertemplate=(
                          "<b>Year:</b> %{customdata[0]}<br>"
                          "<b>" + metric + ":</b> %{y:.2f}<br>"
                          "<b>Month:</b> %{x}<extra></extra>"
                      ))

    return fig


# Aggregate data at the country level
def aggregate_kpi_level(data, state_code):
    # Use the entire dataset if 'USA', otherwise filter by state code
    df = data if state_code == 'USA' else data[data['State Code'] == state_code]

    # Select and aggregate required fields
    df_required = df[['Year', 'Sales', 'Quantity', 'Profit']]
    aggregated_kpi_data = df_required.groupby(['Year']).agg({
        'Sales': 'sum',
        'Quantity': 'sum',
        'Profit': 'sum'
    }).reset_index()

    # Calculate Profit Margin as a percentage of Sales
    aggregated_kpi_data['Profit Margin'] = (
        aggregated_kpi_data['Profit'] / aggregated_kpi_data['Sales'] * 100
    ).round(2)

    # Calculate year-on-year percentage changes for each metric
    for metric in ['Sales', 'Quantity', 'Profit', 'Profit Margin']:
        previous_year_metric = aggregated_kpi_data[metric].shift(
            1)  # Shift to get previous year's data
        change_column_name = f'{metric} Change'

        # Calculate the percentage change from the previous year
        # Adjust for direction of change especially for metrics that can be negative
        aggregated_kpi_data[change_column_name] = (
            (aggregated_kpi_data[metric] - previous_year_metric) /
            abs(previous_year_metric) * 100
            if previous_year_metric.all() != 0 else 0
        ).round(2)

    # Sort the DataFrame by 'Year'
    aggregated_kpi_data.sort_values(by='Year', inplace=True)

    return aggregated_kpi_data


def create_indicator(value, delta, title, is_currency=False, is_percentage=False):

    delta = delta / 100  # Added to get the KPI Display to be working correctly

    color = 'green' if delta >= 0 else 'red'

    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=value,
        number={'prefix': '$' if is_currency else '',
                'suffix': '%' if is_percentage else '', 'font': {'size': 20}},
        delta={
            'reference': value - delta,
            'relative': False,
            'valueformat': '.2%',
            'font': {'size': 15},
            'increasing': {'color': color},
            'decreasing': {'color': color},

        }
    ))

    fig.update_layout(
        height=90,
        margin={'l': 10, 'r': 10, 't': 30, 'b': 10},
        paper_bgcolor="white",
        title={
            'text': 'Gross ' + title,
            'y': 0.9,  # Vertical alignment (the top is 1 and the bottom is 0)
            'x': 0.5,  # Center the title horizontally
            'xanchor': 'center',  # Ensures that the title's x position is the center
            'yanchor': 'top'  # Ensures the title is positioned at the top of the figure
        },
        title_font={'size': 18}
    )

    return fig


def choropleth_dataframe(sales_data, selected_year):
    # Step 1: Filter the data for the selected year
    filtered_data = sales_data[sales_data['Year'] == selected_year]

    # Step 2: Select the required columns
    required_columns = filtered_data[[
        'State', 'State Code', 'Sales', 'Quantity', 'Profit']]

    # Step 3: Aggregate the data by State and State Code
    aggregated_data = required_columns.groupby(['State', 'State Code']).agg({
        'Sales': 'sum',
        'Quantity': 'sum',
        'Profit': 'sum'
    }).reset_index()

    # Step 4: Calculate Profit Margin as a percentage of Sales
    aggregated_data['Profit Margin'] = (
        aggregated_data['Profit'] / aggregated_data['Sales'] * 100).round(2)

    # Return the aggregated data
    return aggregated_data


def choropleth_map_creation(data, metric):
    # Optionally preprocess data if necessary

    fig = px.choropleth(
        data_frame=data,
        locations='State Code',  # Use state codes for locations
        color=metric,  # Data column that determines the color of the map areas
        hover_name='State',  # State names will appear in the tooltip
        hover_data=[metric],  # Additional data to appear in the tooltip
        locationmode='USA-states',  # Set the location mode to USA states
        color_continuous_scale='BuGn',  # Color scale
        scope='usa',  # Limit the map scope to the USA
        labels={metric: metric}  # Label for the color bar
    )

    fig.add_scattergeo(
        locations=data['State Code'],  # codes for states,
        locationmode='USA-states',
        text=data['State Code'],
        mode='text'
    )

    fig.update_layout(
        title_text=f'{metric} by US States',
        geo=dict(lakecolor='white'),
        margin={"r": 0, "t": 30, "l": 0, "b": 0}
    )

    return fig
