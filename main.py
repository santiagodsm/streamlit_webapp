# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# -------------------------------------
# 🔐 AUTHENTICATION + CLIENT SETUP
# -------------------------------------
@st.cache_resource
def get_gspread_client():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds_dict = st.secrets.get("gcp_service_account")
    if not creds_dict:
        raise RuntimeError("Missing gcp_service_account credentials")
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

try:
    client = get_gspread_client()
    sheet_id = "17g9aiOf0mK63tWyIfevKaen_8K_vZXzn078zKjzhq9E"
    sheet = client.open_by_key(sheet_id).worksheet("Agricultores")
except Exception as e:  # handle missing credentials during local development
    sheet = None
    st.warning(
        "Google Sheets integration disabled. "
        "Add credentials to .streamlit/secrets.toml to enable data storage."
    )

# -------------------------------------
# 📥 LOAD DATA
# -------------------------------------
def load_agricultores():
    if sheet is None:
        return pd.DataFrame(
            columns=[
                "Clave",
                "Agricultor",
                "Zona",
                "Email",
                "Teléfono",
                "Dirección",
                "Orden",
            ]
        )
    records = sheet.get_all_records()
    return pd.DataFrame(records)

# -------------------------------------
# ✍️ ADD NEW AGRICULTOR
# -------------------------------------
def add_agricultor(clave, agricultor, zona, email, telefono, direccion, orden):
    if sheet is None:
        st.error("No Google Sheet configured. Entry not saved.")
        return
    new_row = [clave, agricultor, zona, email, telefono, direccion, orden]
    sheet.append_row(new_row)

# -------------------------------------
# 🎯 APP UI
# -------------------------------------
st.title("📋 Registro de Agricultores")

st.subheader("📄 Lista actual")
df = load_agricultores()
st.dataframe(df)

st.subheader("➕ Añadir nuevo agricultor")

with st.form("add_agricultor_form"):
    clave = st.text_input("Clave")
    agricultor = st.text_input("Agricultor")
    zona = st.text_input("Zona")
    email = st.text_input("Email")
    telefono = st.text_input("Teléfono")
    direccion = st.text_input("Dirección")
    orden = st.text_input("Orden")

    submitted = st.form_submit_button("Guardar")

    if submitted:
        if all([clave, agricultor, zona, email, telefono, direccion, orden]):
            add_agricultor(clave, agricultor, zona, email, telefono, direccion, orden)
            st.success(f"Agricultor '{agricultor}' agregado con éxito ✅")
            st.rerun()
        else:
            st.error("Por favor completa todos los campos.")