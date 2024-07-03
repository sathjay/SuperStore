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

    original_sales_data = df.copy()  # Save a copy of the original data

    # Create 'Profit Margin' column and # Round 'Profit Margin' to two decimal places
    df['Profit Margin'] = (df['Profit'] / df['Sales']) * 100
    df['Profit Margin'] = df['Profit Margin'].round(2)

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

    # Any additional preprocessing steps
    sales_data_with_return_and_profit_margin = df.copy()

    return original_sales_data, sales_data_with_return_and_profit_margin
