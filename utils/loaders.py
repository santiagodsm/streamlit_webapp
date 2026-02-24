# =========================================================
# Loaders Utility
# - Provides functions to load data from Google Sheets into pandas DataFrames
# =========================================================

import pandas as pd

def load_sheet_as_df(client, sheet_id, sheet_name):
    """
    Load data from a specific Google Sheets tab into a pandas DataFrame.

    Args:
        client: An authorized gspread client instance.
        sheet_id (str): The ID of the Google Sheet.
        sheet_name (str): The name of the specific worksheet/tab to load.

    Returns:
        pd.DataFrame: A DataFrame containing the data from the specified worksheet.

    Behavior:
        - Opens the Google Sheet using the provided sheet ID.
        - Accesses the specific worksheet/tab by name.
        - Fetches all records as a list of dictionaries and converts them to a DataFrame.
    """
    ws = client.open_by_key(sheet_id).worksheet(sheet_name)
    return pd.DataFrame(ws.get_all_records())