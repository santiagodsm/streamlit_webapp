# =========================================================
# Main Application Entry Point
# - Sets up the Streamlit interface
# - Handles navigation across different modules
# - Manages authentication and shared services
# =========================================================

import streamlit as st
from utils.auth import get_gspread_client
from utils.auth import get_drive_service
from config import SHEET_ID, INGRESAR_DATOS_SHEET_ID

# Import View Modules
import views.gestionar_maestros as gestionar_maestros
import views.ingresar_datos as ingresar_datos
import views.procesar_datos as procesar_datos
import views.visualizar_reportes as visualizar_reportes

# -------------------------
# Initialize External Services
# -------------------------

# Initialize Google Sheets API client
gspread_client = get_gspread_client()

# Initialize Google Drive API client
drive_service = get_drive_service()

# -------------------------
# Sidebar Navigation Setup
# -------------------------

# Display a logo or avatar image at the top of the sidebar
st.sidebar.markdown(
    """
    <div style="text-align: center;">
        <img src="https://24a0ff8439a6c5518b2d-b52a505b3b0736c8f6307a39a7e3ff73.ssl.cf5.rackcdn.com/2300000/2301635/_xsavatar1665423637.jpeg" width="150">
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar title and section navigation
st.sidebar.title("📊 Navegación")
section = st.sidebar.radio(
    "Selecciona una sección:",
    [
        "🗂️ 1. Gestionar Maestros",
        "📝 2. Ingresar Datos",
        "⚙️ 3. Procesar Datos",
        "📈 4. Ver Reportes"
    ]
)

# -------------------------
# Main Section Routing
# -------------------------

# Route the user to the selected page
if section == "🗂️ 1. Gestionar Maestros":
    gestionar_maestros.render(gspread_client, SHEET_ID, drive_service)
elif section == "📝 2. Ingresar Datos":
    ingresar_datos.render(gspread_client, INGRESAR_DATOS_SHEET_ID, drive_service)
elif section == "⚙️ 3. Procesar Datos":
    procesar_datos.render()
elif section == "📈 4. Ver Reportes":
    visualizar_reportes.render(gspread_client, SHEET_ID)