import pandas as pd
import plotly.express as px

# Define options for dropdowns
metrics_options = [{'label': "Days to Ship", 'value': "Days to Ship"},
                   {'label': 'Discount', 'value': 'Discount'},
                   {'label': 'Profit', 'value': 'Profit'},
                   {'label': 'Profit Ratio', 'value': 'Profit Ratio'},
                   {'label': 'Quantity', 'value': 'Quantity'},
                   {'label': 'Returns', 'value': 'Returned'},
                   {'label': 'Sales', 'value': 'Sales'}]


granularity_options = [{'label': gran, 'value': gran} for gran in [
    'Week', 'Quarter', 'Month', 'Year']]
breakdown_options = [{'label': break_down, 'value': break_down} for break_down in [
    'Segment', 'Ship Mode', 'Customer Name', 'Category', 'Sub-Category', 'Product Name']]


def filter_data(dataframe, start_date, end_date, selected_metric, selected_granularity):
    '''Get the filtered dataframe based on the selected date range and granularity.'''
    # Convert start and end date strings to datetime objects
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter the dataframe for dates within the start and end date range
    date_filtered_df = dataframe[(dataframe['Order Date'] >= start_date) & (
        dataframe['Order Date'] <= end_date)]

    # Base columns for grouping
    group_by_list = ['Year']

    # If granularity is not 'Year', add the selected granularity to the columns list
    if selected_granularity != 'Year':
        group_by_list.append(selected_granularity)

    # Determine columns based on selected metric
    if selected_metric == 'Profit Ratio':
        metrics_column = ["Profit", "Sales"]
    else:
        metrics_column = [selected_metric]

    # Combine the metrics column and group_by_list to create the final columns to keep
    columns_to_keep = metrics_column + group_by_list

    # Extract only the necessary columns from the filtered dataframe
    final_filtered_df = date_filtered_df[columns_to_keep]

    # If the selected metric is 'Returned', convert 'Yes' to 1, everything else to 0
    if selected_metric == 'Returned':
        final_filtered_df['Returned'] = final_filtered_df['Returned'].apply(
            lambda x: 1 if x == 'Yes' else 0)

    print(final_filtered_df.columns)

    # Return the dataframe and the group_by_list
    return final_filtered_df, group_by_list


def aggregate_data_for_timeline_graph(final_filtered_df, group_by_list, selected_metric):
    '''Aggregate the filtered data based on the selected metric and group by list.'''
    if selected_metric in ['Profit', 'Sales', 'Returned', 'Quantity']:
        # Perform group by and sum the selected metric
        aggregated_data = final_filtered_df.groupby(group_by_list).agg({
            selected_metric: 'sum'
        }).reset_index()

    elif selected_metric in ['Days to Ship', 'Discount']:
        # Perform group by and calculate the average
        aggregated_data = final_filtered_df.groupby(group_by_list).agg({
            selected_metric: 'mean'
        }).reset_index()
        # Round the results to two decimal places
        aggregated_data[selected_metric] = aggregated_data[selected_metric].round(
            2)

    elif selected_metric == 'Profit Ratio':
        # Ensure the dataframe has the necessary columns
        if 'Sales' in final_filtered_df.columns and 'Profit' in final_filtered_df.columns:
            # Perform group by and sum both Sales and Profit
            aggregated_data = final_filtered_df.groupby(group_by_list).agg({
                'Sales': 'sum',
                'Profit': 'sum'
            }).reset_index()

            # Calculate Profit Ratio and round it to two decimal places
            aggregated_data['Profit Ratio'] = (
                aggregated_data['Profit'] / aggregated_data['Sales'] * 100).round(2)

            # Keep only the necessary columns
            aggregated_data = aggregated_data[group_by_list + ['Profit Ratio']]
        else:
            raise ValueError(
                "Dataframe must contain both 'Sales' and 'Profit' columns for Profit Ratio calculations.")

    else:
        raise ValueError(f"Unsupported metric: {selected_metric}")

    return aggregated_data


def create_combined_date_column(dataframe):
    """
    Dynamically create a 'Date' column in the dataframe based on available time components in the dataframe
    Returns:
    DataFrame: The modified dataframe with a new 'Date' column.
    """
    # Initialize 'Date' as 'Year' first
    if 'Year' in dataframe.columns:
        dataframe['Date'] = dataframe['Year'].astype(str)

    # If 'Month' is available, add it to 'Date'
    if 'Month' in dataframe.columns:
        dataframe['Date'] = dataframe['Date'] + '-' + \
            dataframe['Month'].astype(str).str.zfill(2)

    # If 'Week' is available, format it with 'W' prefix
    if 'Week' in dataframe.columns:
        dataframe['Date'] = dataframe['Year'].astype(
            str) + '-W' + dataframe['Week'].astype(str).str.zfill(2)

    # If 'Quarter' is available, format it with 'Q' prefix
    if 'Quarter' in dataframe.columns:
        dataframe['Date'] = dataframe['Year'].astype(
            str) + '-Q' + dataframe['Quarter'].astype(str)

    return dataframe


def create_line_chart(dataframe, metric):
    """
    Creates a line chart with 'Date' on the x-axis and the specified metric on the y-axis.
    Returns:
    plotly.graph_objs.Figure: The figure object containing the line chart.

    """
    # Generate the line chart
    fig = px.line(
        dataframe,
        x='Date',  # Assuming 'Date' is already in a suitable format for display
        y=metric,
        markers=True,  # Optionally add markers to each data point
        line_shape='linear'  # Ensures the line is straight and does not interpolate
    )

    # Update layout to enhance readability
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title=metric,
        plot_bgcolor='white',  # Sets background color to white
        paper_bgcolor='white',  # Sets surrounding paper color to white
        hovermode='x',  # Enhances hover interaction by highlighting all data for any given x-coordinate
        margin=dict(l=0, r=0, t=25, b=0),
        xaxis=dict(
            showline=True,  # Show x-axis line
            showgrid=False,  # Hide grid lines
            linecolor='black',  # x-axis line color
        ),

        yaxis=dict(
            showline=True,  # Show y-axis line
            showgrid=False,  # Hide grid lines
            linecolor='black',  # y-axis line color
        ),
        title={
            'text': f'Timeline of {metric}',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        titlefont={'size': 15}
    )

    # Customize x-axis ticks and labels for better visualization
    fig.update_xaxes(
        tickangle=45,  # Rotates labels to prevent overlap
        # Treats the x-axis values as categories (important for non-numeric dates)
        type='category'
    )

    return fig


def bubble_chart_dataframe(dataframe, start_date, end_date, selected_metric, metric_list, breakdown):
    '''Prepare the dataframe for the bubble chart based on the selected date range and metric.'''
    # Convert start and end dates to datetime objects
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter the dataframe based on the provided date range
    date_filtered_df = dataframe[(dataframe['Order Date'] >= start_date) & (
        dataframe['Order Date'] <= end_date)]

    # Update 'Returned' column to be numerical
    date_filtered_df['Returned'] = date_filtered_df['Returned'].apply(
        lambda x: 1 if x == 'Yes' else 0)

    # Prepare columns to keep based on metrics list and breakdown
    columns_to_keep = metric_list + [breakdown]
    filtered_df = date_filtered_df[columns_to_keep]

    # Define columns for average aggregation
    avg_agg_df_columns = ['Days to Ship', 'Discount', breakdown]
    avg_agg_df = filtered_df[avg_agg_df_columns].groupby(
        breakdown).mean().reset_index()
    avg_agg_df['Days to Ship'] = avg_agg_df['Days to Ship'].round(2)
    avg_agg_df['Discount'] = avg_agg_df['Discount'].round(2)

    # Define columns for sum aggregation
    sum_agg_df_columns = ['Profit', 'Quantity', 'Sales', 'Returned', breakdown]
    sum_agg_df = filtered_df[sum_agg_df_columns].groupby(
        breakdown).sum().reset_index()

    # Calculate 'Profit Ratio'
    sum_agg_df['Profit Ratio'] = (
        sum_agg_df['Profit'] / sum_agg_df['Sales'] * 100).round(2)

    # Merge the average and sum aggregated dataframes on the breakdown column
    final_bubble_chart_df = pd.merge(avg_agg_df, sum_agg_df, on=breakdown)

    return final_bubble_chart_df


def preprocess_data_for_bubble_chart(df, size_metric):
    '''Preprocess the data for the bubble chart by ensuring all size values are positive.'''
    # Ensure all size values are positive; replace negative values with a small positive value
    df[size_metric] = df[size_metric].apply(lambda x: 0.2 if x < 0 else x)
    return df


def create_bubble_chart(bubble_chart_df, x_axis, y_axis, size_metric, color_breakdown):
    '''Create a bubble chart based on the provided data and parameters.
    Returns: plotly.graph_objs.Figure: The figure object containing the bubble chart.'''

    # Preprocess the dataframe to adjust size metric values
    bubble_chart_df = preprocess_data_for_bubble_chart(
        bubble_chart_df, size_metric)

    # Create the bubble chart using Plotly Express
    fig = px.scatter(
        bubble_chart_df,
        x=x_axis,
        y=y_axis,
        size=size_metric,
        color=color_breakdown,
        hover_name=color_breakdown,  # Optionally set hover data
        size_max=60  # Adjust the max size to fit your design

    )

    # Enhance layout
    fig.update_layout(
        xaxis_title=x_axis,
        yaxis_title=y_axis,
        legend_title=color_breakdown,
        plot_bgcolor='white',  # Set background color to white
        paper_bgcolor='white',  # Set the area around the graph to white
        margin=dict(l=0, r=0, t=20, b=0),
        xaxis=dict(
            showline=True,  # Show x-axis line
            showgrid=False,  # Hide grid lines
            linecolor='black',  # x-axis line color
        ),

        yaxis=dict(
            showline=True,  # Show y-axis line
            showgrid=False,  # Hide grid lines
            linecolor='black',  # y-axis line color
        ),
        title={
            'text': f"Bubble Chart of {size_metric} by {color_breakdown}",
            'y': 0.97,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        titlefont={'size': 15}
    )

    return fig
