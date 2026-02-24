# =========================================================
# Auth Utility
# - Provides authentication handlers for Google Sheets and Google Drive APIs
# - Supports both Streamlit Cloud (secrets) and local development (credentials.json)
# =========================================================

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import json
from googleapiclient.discovery import build

def get_credentials():
    """
    Load Google API credentials dynamically.

    Behavior:
        - If running in Streamlit Cloud, credentials are loaded from st.secrets.
        - If running locally, credentials are loaded from a local 'credentials.json' file.

    Returns:
        ServiceAccountCredentials: Authorized credentials object for API access.
    """
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    try:
        # Attempt to load credentials from Streamlit's secure secrets manager
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    except st.errors.StreamlitAPIException:
        # Fallback to loading credentials locally when secrets are not available
        with open("credentials.json") as f:
            creds_dict = json.load(f)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

    return creds

def get_gspread_client():
    """
    Initialize and return a gspread client authorized to interact with Google Sheets.

    Returns:
        gspread.Client: An authenticated gspread client instance.
    """
    creds = get_credentials()
    return gspread.authorize(creds)

def get_drive_service():
    """
    Initialize and return a Google Drive service client.

    Returns:
        googleapiclient.discovery.Resource: Authenticated Drive API service resource.
    """
    creds = get_credentials()
    return build('drive', 'v3', credentials=creds)