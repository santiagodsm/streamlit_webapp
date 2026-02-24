# =========================================================
# Records Utility
# - Provides helper functions to find, add, update, and delete records in Google Sheets
# - Also includes validation functions for numeric and currency types
# =========================================================

def find_row_index_by_key(df, key_col, key_value):
    """
    Find the index of a row where the value in key_col matches key_value.

    Args:
        df (pd.DataFrame): The DataFrame to search.
        key_col (str): The column to match on.
        key_value (str): The value to find.

    Returns:
        int: The row index if found, None otherwise.
    """
    match = df[df[key_col] == key_value]
    return match.index[0] if not match.empty else None

def update_row(ws, row_idx: int, values: list):
    """
    Update an existing row in the Google Sheet with new values.

    Args:
        ws: gspread worksheet object.
        row_idx (int): Row index to update (1-based index in Sheets).
        values (list): List of values to write into the row.

    Behavior:
        Updates from column A to the necessary last column based on values length.
    """
    col_count = len(values)
    end_col = chr(64 + col_count)  # ASCII A=65, assumes up to 'Z'
    ws.update(f"A{row_idx}:{end_col}{row_idx}", [values])

def delete_row(ws, row_idx: int):
    """
    Delete a row from the worksheet based on the row index.

    Args:
        ws: gspread worksheet object.
        row_idx (int): Row index to delete.
    """
    ws.delete_rows(row_idx)

def add_record(df, ws, new_row_dict, key_col):
    """
    Add a new record to the worksheet if the key does not already exist.

    Args:
        df (pd.DataFrame): DataFrame to check for duplicates.
        ws: gspread worksheet object.
        new_row_dict (dict): New record data mapped by column.
        key_col (str): Column to enforce uniqueness.

    Raises:
        ValueError: If the key already exists in the DataFrame.
    """
    key_value = new_row_dict.get(key_col)
    if key_value in df[key_col].astype(str).values:
        raise ValueError(f"{key_col} '{key_value}' ya existe.")
    ordered_values = [new_row_dict.get(col, "") for col in df.columns]
    ws.append_row(ordered_values)

def edit_record(df, ws, key_col, key_value, updated_dict):
    """
    Edit an existing record identified by a unique key.

    Args:
        df (pd.DataFrame): DataFrame to locate the record.
        ws: gspread worksheet object.
        key_col (str): Column used as unique key.
        key_value (str): Value to find and update.
        updated_dict (dict): Updated field values.

    Raises:
        ValueError: If no matching record is found.
    """
    match = df[df[key_col] == key_value]
    if match.empty:
        raise ValueError(f"{key_col} '{key_value}' no encontrado.")
    row_idx = match.index[0] + 2  # +2 to account for 1-based indexing and header
    ordered_values = [updated_dict.get(col, "") for col in df.columns]
    col_count = len(ordered_values)
    end_col = chr(64 + col_count)
    ws.update(f"A{row_idx}:{end_col}{row_idx}", [ordered_values])

def delete_record_by_key(df, ws, key_col, key_value):
    """
    Delete a record from the worksheet identified by a unique key.

    Args:
        df (pd.DataFrame): DataFrame to locate the record.
        ws: gspread worksheet object.
        key_col (str): Column used as unique key.
        key_value (str): Value to find and delete.

    Raises:
        ValueError: If no matching record is found.
    """
    match = df[df[key_col] == key_value]
    if match.empty:
        raise ValueError(f"{key_col} '{key_value}' no encontrado.")
    row_idx = match.index[0] + 2
    ws.delete_rows(row_idx)



def delete_records_by_column(ws, column_name, match_value):
    """
    Delete all rows from the worksheet where the specified column matches the given value.

    Args:
        ws: gspread worksheet object.
        column_name (str): The name of the column to match.
        match_value (str): The value to delete rows for.
    """
    import pandas as pd
    df = pd.DataFrame(ws.get_all_records())
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in worksheet.")
    match_indices = df[df[column_name] == match_value].index
    for idx in reversed(match_indices):
        ws.delete_rows(idx + 2)  # +2 accounts for header row and 0-indexing