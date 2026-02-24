# =========================================================
# Validators Utility
# - Provides reusable functions for input validation
# - Ensures email, phone, uniqueness, required fields,
#   currency formats, and numeric formats are properly validated
# =========================================================

import re
import pandas as pd

def is_valid_email(email: str) -> bool:
    """
    Validate if the input string is a valid email address format.

    Args:
        email (str): Email address to validate.

    Returns:
        bool: True if the email format is valid, False otherwise.
    """
    pattern = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
    return bool(re.match(pattern, email.strip()))

def is_valid_phone(phone: str) -> bool:
    """
    Validate if the input string is a valid phone number.

    A valid phone number must have between 7 and 15 digits and can optionally start with '+'.

    Args:
        phone (str): Phone number to validate.

    Returns:
        bool: True if the phone format is valid, False otherwise.
    """
    pattern = r'^\+?\d{7,15}$'
    return bool(re.match(pattern, phone.strip()))

def is_unique(df: pd.DataFrame, column: str, value: str) -> bool:
    """
    Check if a given value is unique within a specified DataFrame column.

    Args:
        df (pd.DataFrame): DataFrame to check against.
        column (str): Column name where uniqueness should be checked.
        value (str): Value to check for uniqueness.

    Returns:
        bool: True if the value is unique (not present), False otherwise.
    """
    return value not in df[column].astype(str).values

def is_required(value: str) -> bool:
    """
    Validate that a given string value is not empty or just whitespace.

    Args:
        value (str): The string value to validate.

    Returns:
        bool: True if value is not empty, False otherwise.
    """
    return bool(value.strip())

def is_currency(value: str) -> bool:
    """
    Validate if input can be interpreted as a numeric currency value.
    Accepts currency symbols and commas.

    Args:
        value (str): Currency value as a string.

    Returns:
        bool: True if the value can be parsed as float, False otherwise.
    """
    try:
        normalized = str(value).replace('$', '').replace(',', '').strip()
        float(normalized)
        return True
    except (ValueError, TypeError):
        return False

def is_percentage(value: str) -> bool:
    """
    Validate if input can be interpreted as a numeric percentage value.
    Accepts percentage signs.

    Args:
        value (str): Percentage value as a string.

    Returns:
        bool: True if the value can be parsed as float, False otherwise.
    """
    try:
        normalized = str(value).replace('%', '').strip()
        float(normalized)
        return True
    except (ValueError, TypeError):
        return False

def is_numeric(value: str) -> bool:
    """
    Validate if a string can be converted to a numeric format (integer or float).

    Args:
        value (str): Value to validate.

    Returns:
        bool: True if the value can be parsed as a number, False otherwise.
    """
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False