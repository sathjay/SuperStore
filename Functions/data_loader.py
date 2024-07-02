import pandas as pd


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

    # Merge or join with returns data if needed
    # df = df.merge(df_return, on='Order ID', how='left')

    # Any additional preprocessing steps
    original_sales_data = df.copy()
    returns_data = df_return.copy()

    return original_sales_data, returns_data
