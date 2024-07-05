import pandas as pd

# Define options for dropdowns
metrics_options = [{'label': metric, 'value': metric} for metric in [
    'Days to Ship', 'Discount', 'Profit', 'Profit Ratio', 'Quantity', 'Returned', 'Sales']]
granularity_options = [{'label': gran, 'value': gran} for gran in [
    'Week', 'Quarter', 'Month', 'Year']]
breakdown_options = [{'label': break_down, 'value': break_down} for break_down in [
    'Segment', 'Ship Mode', 'Customer Name', 'Category', 'Sub-Category', 'Product Name']]


def filter_data(dataframe, start_date, end_date, selected_metric, selected_granularity):
    # Convert start and end date strings to datetime objects
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    final_filtered_df = pd.DataFrame()

    # Filter the dataframe for dates within the start and end date range
    date_filtered_df = dataframe[(dataframe['Order Date'] >= start_date) & (
        dataframe['Order Date'] <= end_date)]

    # Base columns include the metric and the Year always
    columns_to_keep = [selected_metric, 'Year']

    # If granularity is not 'Year', add the selected granularity to the columns list
    if selected_granularity != 'Year':
        columns_to_keep.append(selected_granularity)

    # Filter the dataframe to only include the necessary columns
    final_filtered_df = date_filtered_df[columns_to_keep]

    return final_filtered_df


def get_groupby_columns(dataframe, selected_metric):
    # Create a list of columns for grouping by removing the selected_metric
    groupby_columns = [
        col for col in dataframe.columns if col != selected_metric]
    return groupby_columns


def aggregate_data(dataframe, groupby_columns, selected_metric):
    # Define the aggregation dictionary based on the metric
    aggregation_methods = {
        'Days to Ship': 'mean',
        'Discount': 'mean',
        'Profit': 'sum',
        'Quantity': 'sum',
        'Sales': 'sum',
        # Only aggregate if 'Returned' is the selected metric
        'Returned': ('sum' if selected_metric == 'Returned' else None)
    }

    # Check if the selected metric is 'Returned' to count 'Yes'
    if selected_metric == 'Returned':
        # Convert 'Returned' to a numeric value where 'Yes' is 1 and otherwise 0
        dataframe['Returned'] = dataframe['Returned'].apply(
            lambda x: 1 if x == 'Yes' else 0)

    # Determine the aggregation method from the dictionary, default to sum if not specified
    agg_method = aggregation_methods.get(selected_metric, 'sum')

    # Perform the aggregation
    aggregated_df = dataframe.groupby(groupby_columns).agg(
        {selected_metric: agg_method}).reset_index()

    return aggregated_df
