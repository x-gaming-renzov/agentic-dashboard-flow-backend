import pandas as pd

def extract_columns_and_values(df: pd.DataFrame, chartType: str) -> tuple:
    """
    Extracts columns and values from a Pandas DataFrame.

    :param df: The Pandas DataFrame to extract data from.
    :return: A tuple containing the list of column names and the list of tuples with row values.
    """
    try:
        if df.empty:
            print("The provided DataFrame is empty.")
            return [], []

        # Extract the column names
        columns = df.columns.tolist()

        if chartType == 'line':
            # Extract the row values
            x_values = df[columns[0]].tolist()
            y_values = df[columns[1]].tolist()
            values = list(zip(x_values, y_values))
        elif chartType == 'bar':
            # Extract the row values
            x_values = df[columns[0]].tolist()
            y_values = df[columns[1]].tolist()
            values = list(zip(x_values, y_values))
        elif chartType == 'pie':
            # Extract the row values
            x_values = df[columns[0]].tolist()
            y_values = df[columns[1]].tolist()
            z_values = df[columns[2]].tolist()
            values = list(zip(x_values, y_values, z_values))
        elif chartType == 'metric':
            # Extract the row values
            x_values = df[columns[0]].tolist()
            values = list(zip(x_values))
        else:
            print(f"Unsupported chart type: {chartType}")
            return [], []
    
        return columns, values

    except Exception as e:
        print("Error while extracting columns and values from DataFrame", e)
        return [], []