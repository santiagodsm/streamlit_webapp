# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials securely from st.secrets
creds_dict = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Open the spreadsheet
sheet_id = "17g9aiOf0mK63tWyIfevKaen_8K_vZXzn078zKjzhq9E"
sheet = client.open_by_key(sheet_id).worksheet("Agricultores")

# Load and display data
data = sheet.get_all_records()
df = pd.DataFrame(data)

st.title("Datos de Agricultores")
st.dataframe(df)