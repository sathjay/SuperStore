import pandas as pd

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


def bubble_chart_dataframe(dataframe, start_date, end_date, selected_metric, metric_list, breakdown):
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
