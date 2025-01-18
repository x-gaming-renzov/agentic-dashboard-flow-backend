import logging
import re
import pandas
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler('app.log')  # File output
    ]
)
logger = logging.getLogger(__name__)

def log_error(message, exception):
    """Log errors with consistent formatting."""
    logger.error(f"{message}: {str(exception)}")

import pandas as pd

def extract_columns_and_values(df: pd.DataFrame):
    """
    Extracts columns and values from a Pandas DataFrame.

    :param df: The Pandas DataFrame to extract data from.
    :return: A tuple containing the list of column names and the list of tuples with row values.
    """
    try:
        if df.empty:
            logging.warning("The provided DataFrame is empty.")
            return [], []

        # Extract the column names
        columns = df.columns.tolist()

        # Extract the values as a list of tuples
        # Convert int64 to float during tuple creation
        values = [tuple(float(val) if isinstance(val, np.int64) else val for val in row) for row in df.values]

        logging.info(f"Extracted {len(values)} rows and {len(columns)} columns from the DataFrame.")
        return columns, values

    except Exception as e:
        log_error("Error while extracting columns and values from DataFrame", e)
        return [], []
