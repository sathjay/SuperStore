import pandas as pd
import plotly  # (version 4.5.4) pip install plotly==4.5.4


def create_query(selected_segment, selected_category, selected_sub_category, selected_region, selected_state, selected_city):
    # List to hold individual query parts
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
    # Use the query string to filter the DataFrame
    if query_string:
        filtered_df = df.query(query_string)
    else:
        # If no query string, return the unfiltered DataFrame
        filtered_df = df
    return filtered_df
