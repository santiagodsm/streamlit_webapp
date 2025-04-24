# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Define scope and authorize with credentials.json
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Use the spreadsheet ID
sheet_id = "17g9aiOf0mK63tWyIfevKaen_8K_vZXzn078zKjzhq9E"

# Open the spreadsheet by ID and select the 'agricultores' sheet
sheet = client.open_by_key(sheet_id).worksheet("Agricultores")

# Get all records as a DataFrame
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Show in Streamlit
st.title("Datos de Agricultores")
st.dataframe(df)