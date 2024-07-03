import pandas as pd
from Functions.USA_map import state_codes


def load_and_preprocess_data(file_path):
    # Load the data
    df = pd.read_excel(file_path, sheet_name='Orders')
    df_return = pd.read_excel(file_path, sheet_name='Returns')

    # Performing  type conversions here

    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])

    df['Sales'] = df['Sales'].astype(float).round(2)
    df['Discount'] = df['Discount'].astype(float).round(2)
    df['Profit'] = df['Profit'].astype(float).round(2)
    df['Quantity'] = df['Quantity'].astype(int)

    # Map state names to state codes
    if 'State' in df.columns:
        df['State Code'] = df['State'].map(state_codes)

    # Extract the year from 'Order Date' and get unique years
    df['Year'] = df['Order Date'].dt.year
    unique_years = df['Year'].unique()
    unique_years.sort()
    unique_years = unique_years[::-1]  # Reverse the order of years

    # Merge or join with returns data if needed

    df = df.merge(df_return[['Order ID', 'Returned']],
                  on='Order ID', how='left')
    df['Returned'] = df['Returned'].fillna('No')

    df_return_yes = df_return[df_return['Returned'] == 'Yes']['Order ID']
    df_merged_yes = df[df['Returned'] == 'Yes']['Order ID']

    comparison_result = df_merged_yes.isin(df_return_yes).all()

    if comparison_result:
        print("All 'Returned' values are correctly populated.")
    else:
        print("Some 'Returned' values are incorrectly populated.")

    sales_data = df.copy()  # Save a copy of the original data

    return sales_data, unique_years
