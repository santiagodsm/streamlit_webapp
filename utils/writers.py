# =========================================================
# Writers Utility
# - Provides functions to write and append data to Google Sheets
# =========================================================

def append_row_to_sheet(client, sheet_id, sheet_name, row_values: list):
    """
    Append a new row to a specific worksheet (tab) inside a Google Sheet.

    Args:
        client: Authorized gspread client instance.
        sheet_id (str): The unique ID of the Google Sheet.
        sheet_name (str): The name of the worksheet/tab where the row should be appended.
        row_values (list): A list containing the values for each column in the new row.

    Behavior:
        - Opens the specified Google Sheet by its ID.
        - Selects the worksheet/tab by its name.
        - Appends the provided row values as a new record at the bottom of the worksheet.

    Example:
        append_row_to_sheet(client, "sheet_id", "Agricultores", ["001", "Juan Perez", "Zona Norte", "email@example.com"])
    """
    ws = client.open_by_key(sheet_id).worksheet(sheet_name)
    ws.append_row(row_values)