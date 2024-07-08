import pandas as pd
import plotly.express as px
import calendar
import plotly.graph_objects as go
from plotly.subplots import make_subplots


metric_dropdown = [
    {'label': 'Sales', 'value': 'Sales'},
    {'label': 'Quantity', 'value': 'Quantity'},
    {'label': 'Profit', 'value': 'Profit'},
    {'label': 'Profit Margin', 'value': 'Profit Margin'}

]

category_dropdown = [
    {'label': 'Customer', 'value': 'Customer Name'},
    {'label': 'State', 'value': 'State'},
    {'label': 'City', 'value': 'City'},
    {'label': 'Sub-Category', 'value': 'Sub-Category'},
    {'label': 'Product', 'value': 'Product Name'}
]


def update_title(selected_year, selected_state=None):
    if selected_year is not None:
        return f"{selected_year} SuperStore Metric for {selected_state}"
    return "SuperStore Executive Summary"


def update_map_title(selected_year, metric):
    if selected_year is not None:
        return f"{selected_year} {metric} Overview by US States"
    return "Overview by States"


def update_metric_trends_title(selected_year, selected_state=None):
    if selected_year is not None:
        return f"{selected_year} Metric trends for {selected_state}"
    return "Metric trends"


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


def fill_missing_months(data):

    # Added this function beacuse the data was not being displayed correctly
    # Line Chart was not able to display the data correctly with missing months.

    month_names = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
        5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
        9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    }

    all_months = pd.DataFrame({'Month': range(1, 13)})
    all_months['Month'] = all_months['Month'].map(month_names)

    # Merge with all_months DataFrame to find missing months
    data = all_months.merge(data, on='Month', how='left').fillna({
        'Sales': 0,  # Assuming 0 for missing data; adjust as necessary
        'Quantity': 0,
        'Profit': 0,
        'Profit Margin': 0  # Include this only if you use this metric
    })

    return data


def create_line_chart(current_data, previous_data, metric):

    current_data = fill_missing_months(current_data)
    previous_data = fill_missing_months(
        previous_data) if previous_data is not None else None
    # Create a new figure object
    fig = go.Figure()

    # Plot current year data
    fig.add_trace(go.Scatter(
        x=current_data['Month'],
        y=current_data[metric],
        mode='lines+markers',
        name=str(current_data['Year'].iloc[0]),
        line=dict(color='darkblue'),
        marker=dict(color='darkblue', size=7),
        hoverinfo='text',
        hovertext=[
            "Year: {}<br>{}: {:.2f}<br>Month: {}".format(
             current_data['Year'].iloc[0], metric, y, month
            )
            for month, y in zip(current_data['Month'], current_data[metric])
        ]
    ))

    # Plot previous year data if available
    if previous_data is not None:
        fig.add_trace(go.Scatter(
            x=previous_data['Month'],
            y=previous_data[metric],
            mode='lines+markers',
            name=str(previous_data['Year'].iloc[0]),
            line=dict(color='lightgrey'),
            marker=dict(color='lightgrey', size=7),
            hoverinfo='text',
            hovertext=[
                "Year: {}<br>{}: {:.2f}<br>Month: {}".format(
                    previous_data['Year'].iloc[0], metric, y, month
                )
                for month, y in zip(previous_data['Month'], previous_data[metric])
            ]
        ))

    # Update layout for the chart
    fig.update_layout(
        plot_bgcolor='white',  # Background color
        paper_bgcolor='white',  # Background color around the chart
        showlegend=False,  # Optionally turn on the legend
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
            tickvals=[1, 4, 7, 10],
            ticktext=['Jan', 'Apr', 'Jul', 'Oct'],
            range=[0.5, 12.5]  # Adjust the range to encompass all months
        ),
        title={
            'text': f"{metric} Over Time",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        titlefont={'size': 15}
    )

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

    fig = go.Figure()

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
        height=80,
        margin={'l': 10, 'r': 10, 't': 26, 'b': 10},
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


def choropleth_map_creation(data, metric, year):
    # Optionally preprocess data if necessary

    fig = go.Figure()

    fig = px.choropleth(
        data_frame=data,
        locations='State Code',  # Use state codes for locations
        color=metric,  # Data column that determines the color of the map areas
        hover_name='State',  # State names will appear in the tooltip
        hover_data=[metric],  # Additional data to appear in the tooltip
        locationmode='USA-states',  # Set the location mode to USA states
        color_continuous_scale='YlGnBu',  # Color scale
        scope='usa',  # Limit the map scope to the USA
        labels={metric: metric}  # Label for the color bar
    )

    # fig.add_scattergeo(
    #     locations=data['State Code'],  # codes for states,
    #     locationmode='USA-states',
    #     text=data['State Code'],
    #     mode='text'
    # )

    fig.update_layout(
        geo=dict(lakecolor='white'),
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        coloraxis_colorbar=dict(
            x=0.87  # Adjust this value as needed to move the color scale inward
        )
    )

    return fig


def key_figures(sales_data, year, metric, category):

    fig = go.Figure()
    combined_data = pd.DataFrame()

    # Step 1: Filter data for the selected year
    filtered_data = sales_data[sales_data['Year'] == year]

    columns_to_keep = ['Year', category, metric]
    filtered_data = filtered_data[columns_to_keep]

    # Step 2: Group by the category and sum the metric
    grouped_data = filtered_data.groupby(category).agg({
        metric: 'sum'
    }).reset_index()

    # Round the metric to the nearest integer
    grouped_data[metric] = grouped_data[metric].round(0)

    # Step 3: Sort the data by the metric to get top and bottom performers
    top_performers = grouped_data.nlargest(5, metric)
    bottom_performers = grouped_data.nsmallest(5, metric)

    fig = go.Figure()

    # Combine top and bottom for plotting
    combined_data = pd.concat(
        [top_performers, bottom_performers]).sort_values(by=metric)

    # Step 4: Create a horizontal bar graph
    fig = px.bar(combined_data, x=metric, y=category, orientation='v', color=metric, color_continuous_scale='BuGn',
                 title=f"Top & Bottom 5 {category} in {year} by {metric}")

    # Update layout for clarity
    fig.update_layout(
        yaxis=dict(categoryorder='total ascending',
                   showline=True,  # Show y-axis line
                   showgrid=False,
                   ),
        xaxis=dict(
            showline=True,  # Show y-axis line
            showgrid=False,
        ),

        xaxis_title=metric,
        yaxis_title=category,
        coloraxis_showscale=False,
        plot_bgcolor='rgba(0,0,0,0)',  # Make background transparent
        # Make the area around the graph transparent
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,  # Optionally hide the legend if not needed


        xaxis_tickformat=',.2f'  # Format the metric values for better readability
    )

    return fig
