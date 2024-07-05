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
