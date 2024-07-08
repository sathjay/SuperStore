import pandas as pd
from Functions.USA_map import state_codes


def load_and_preprocess_data(file_path):
    '''Load the data from the Excel file and preprocess it. Return the data and unique years list'''
    # Load the data
    df = pd.read_excel(file_path, sheet_name='Orders')
    df_return = pd.read_excel(file_path, sheet_name='Returns')

    # Performing  type conversions here

    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])

    df['Sales'] = df['Sales'].astype(float).round(2)
    df['Discount'] = (df['Discount'].astype(float) * 100).round(2)
    df['Profit'] = df['Profit'].astype(float).round(2)
    df['Quantity'] = df['Quantity'].astype(int)

    # Map state names to state codes
    if 'State' in df.columns:
        df['State Code'] = df['State'].map(state_codes)

    # Extract the year from 'Order Date' and get unique years
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.month

    # Sort data by 'Year' and 'Month'
    df.sort_values(by=['Year', 'Month'], inplace=True)

    unique_years = df['Year'].unique()
    unique_years.sort()
    unique_years = unique_years[::-1]  # Reverse the order of years

    # Merge or join with returns data if needed

    df = df.merge(df_return[['Order ID', 'Returned']],
                  on='Order ID', how='left')
    df['Returned'] = df['Returned'].fillna('No')

    df.sort_values(by='Order Date', inplace=True)

    df_return_yes = df_return[df_return['Returned'] == 'Yes']['Order ID']
    df_merged_yes = df[df['Returned'] == 'Yes']['Order ID']

    comparison_result = df_merged_yes.isin(df_return_yes).all()

    if comparison_result:
        print("All 'Returned' values are correctly populated.")
    else:
        print("Some 'Returned' values are incorrectly populated.")

    sales_data = df.copy()  # Save a copy of the original data

    return sales_data, unique_years


def add_week_and_quarter(sales_data):
    '''Add Week' and Quarter columns to the DataFrame. Return the updated DataFrame.'''
    # Add 'Week' column using ISO week number
    sales_data['Week'] = sales_data['Order Date'].dt.isocalendar().week

    # Add 'Quarter' column
    sales_data['Quarter'] = sales_data['Order Date'].dt.quarter

    # Calculate the number of days to ship
    sales_data['Days to Ship'] = (
        sales_data['Ship Date'] - sales_data['Order Date']).dt.days

    sales_data.sort_values(by='Order Date', inplace=True)
    return sales_data


def add_week_and_quarter_for_table_page(sales_data):
    '''Add Week and Quarter columns to the DataFrame. Return the updated DataFrame.
    The Columns Ship Mode, Customer Name, and Sub-Category are renamed to ShipMode, CustomerName, and SubCategory respectively.'''

    # Add 'Week' column using ISO week number
    sales_data['Week'] = sales_data['Order Date'].dt.isocalendar().week

    # Add 'Quarter' column
    sales_data['Quarter'] = sales_data['Order Date'].dt.quarter

    # Calculate the number of days to ship
    sales_data['Days to Ship'] = (
        sales_data['Ship Date'] - sales_data['Order Date']).dt.days

    sales_data = sales_data.rename(columns={'Ship Mode': 'ShipMode',
                                            'Customer Name': 'CustomerName',
                                            'Sub-Category': 'SubCategory',
                                            })

    sales_data.sort_values(by='Order Date', inplace=True)
    return sales_data
