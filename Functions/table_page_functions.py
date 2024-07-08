import pandas as pd
import plotly  # (version 4.5.4) pip install plotly==4.5.4


def create_query(selected_segment, selected_category, selected_sub_category, selected_region, selected_state, selected_city):
    '''Create a query string based on the selected filters.'''
    query_parts = []

    # Append query part for each filter if the filter is not None
    if selected_segment:
        query_parts.append('Segment == "{}"'.format(selected_segment))
    if selected_category:
        query_parts.append('Category == "{}"'.format(selected_category))
    if selected_sub_category:
        query_parts.append(
            'SubCategory == "{}"'.format(selected_sub_category))
    if selected_region:
        query_parts.append('Region == "{}"'.format(selected_region))
    if selected_state:
        query_parts.append('State == "{}"'.format(selected_state))
    if selected_city:
        query_parts.append('City == "{}"'.format(selected_city))

    # Join all parts into a single query string using 'and'
    query_string = ' and '.join(query_parts)
    return query_string


def filter_dataframe(df, query_string):
    '''Filter the DataFrame based on the query string.'''
    # Use the query string to filter the DataFrame
    if query_string:
        filtered_df = df.query(query_string)
    else:
        # If no query string, return the unfiltered DataFrame
        filtered_df = df
    return filtered_df


def validation_and_display_message(sales_data_with_q_info, order_id, customer_name, product, quantity, price):
    '''Validate the input fields and display a message based on the validation.
    Check whether the input could be inserted into the DataFrame.'''
    # Validate all input fields are entered'

    message = ''
    data_insert_flag = False  # Flag to check if data can be inserted

    if not all([order_id, customer_name, product, quantity, price]):
        message = "Please fill in all fields to add a new entry."
        return message, data_insert_flag

    # Validate quantity and price
    try:
        quantity = float(quantity)
        price = float(price)
        if quantity <= 0:
            message = "Quantity must be a positive number."
            return message, data_insert_flag
    except ValueError:
        message = "Quantity and Price fields must be numbers."
        return message, data_insert_flag

    # Check for duplicate Order ID
    if sales_data_with_q_info['Order ID'].eq(order_id).any():
        message = "Duplicate entry not added: Order ID {} already exists.".format(
            order_id)

        return message, data_insert_flag

    message = "New entry added successfully for Order ID: {}".format(order_id)
    data_insert_flag = True

    return message, data_insert_flag
