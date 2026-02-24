# =========================================================
# Gestionar Maestros View
# - Handles navigation between different master data sets
# - Displays data management options (Agricultores, Clientes, etc.)
# - Routes to the appropriate management modules
# =========================================================

import streamlit as st
from utils.loaders import load_sheet_as_df
from config import MAESTROS_PASSWORD
from views.maestros import agricultores  # Import module for agricultores management
from views.maestros import clientes      # Import module for clientes management
from views.maestros import productos     # Import module for productos esparrago management
from views.maestros import comisiones    # Import module for comisiones management
from views.maestros import cajas         # Import module for cajas management

# Dictionary mapping master data labels to corresponding sheet names
MASTER_SHEETS = {
    "Agricultores": "Agricultores",
    "Clientes": "Clientes",
    "Productos Esparrago": "Producto_Esparrago",
    "Comisiones": "Comisiones",
    "Cajas": "Cajas"
}

def render(client, sheet_id, drive_service):
    """Main rendering function for master data management."""

    # Display the page title
    st.title("🗂️ Gestión de Datos Maestros")

    # Inject custom CSS to style the button bar
    st.markdown(
        """
        <style>
        .button-bar {
            background-color: black;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Password gate to protect master data management
    if "access_granted" not in st.session_state:
        st.session_state["access_granted"] = False

    if not st.session_state["access_granted"]:
        if not MAESTROS_PASSWORD:
            st.error("MAESTROS_PASSWORD no está configurado. Configura la variable de entorno.")
            return
        password = st.text_input("🔒 Introduce la contraseña para gestionar maestros:", type="password")
        if password == MAESTROS_PASSWORD:
            st.session_state["access_granted"] = True
            st.success("Acceso concedido. Ahora puedes gestionar maestros.")
        else:
            st.warning("Introduce la contraseña para ver las opciones de gestión.")
            return

    # Render the button bar for master data navigation
    with st.container():
        st.markdown("<div class='button-bar'>", unsafe_allow_html=True)
        cols = st.columns(len(MASTER_SHEETS))
        for idx, (label, sheet_name) in enumerate(MASTER_SHEETS.items()):
            with cols[idx]:
                if st.button(label, key=f"btn_{label}"):
                    # Store the selected master data type in session state
                    st.session_state["selected_master"] = sheet_name
        st.markdown("</div>", unsafe_allow_html=True)

    # Retrieve the selected master sheet from session state
    sheet_name = st.session_state.get("selected_master")
    if sheet_name:
        # Display the selected catalog
        st.markdown(f"### 📋 Catálogo seleccionado: **{sheet_name}**")
        if sheet_name == "Agricultores":
            agricultores.render(client, sheet_id)
        elif sheet_name == "Clientes":
            clientes.render(client, sheet_id, drive_service)
        elif sheet_name == "Producto_Esparrago":
            productos.render(client, sheet_id)
        elif sheet_name == "Comisiones":
            # Route to the comisiones module render function
            comisiones.render(client, sheet_id)
        elif sheet_name == "Cajas":
            # Route to the cajas module render function
            cajas.render(client, sheet_id)
        else:
            # For non-module masters, attempt to load and display the sheet
            try:
                df = load_sheet_as_df(client, sheet_id, sheet_name)
                st.dataframe(df)
            except Exception as e:
                st.error(f"No se pudo cargar la hoja '{sheet_name}'")
                st.exception(e)