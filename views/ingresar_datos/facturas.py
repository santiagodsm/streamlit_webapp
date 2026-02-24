"""This module provides a Streamlit interface for managing invoices (facturas). 
Users can add invoice headers and details, upload related documents, and save the data to Google Sheets and Google Drive.
"""

import streamlit as st
import pandas as pd
import time
from utils.facturas_helpers import (
    save_uploaded_file_to_drive,
    save_header_factura,
    save_detalle_facturas,
    load_precio_base,
    prepare_detalle_input_table
)
from utils.loaders import load_sheet_as_df
from config import SHEET_ID, INGRESAR_DATOS_SHEET_ID, FOLDER_ID_FACTURAS
from datetime import datetime
from utils import validators

# Caching wrappers to avoid quota errors
@st.cache_data(ttl=600)
def get_clientes_df(_client):
    # Load the 'Clientes' sheet as a DataFrame for the given client
    return load_sheet_as_df(_client, SHEET_ID, "Clientes")

@st.cache_data(ttl=600)
def get_productos_df(_client):
    # Load the 'Producto_Esparrago' sheet as a DataFrame for the given client
    return load_sheet_as_df(_client, SHEET_ID, "Producto_Esparrago")

@st.cache_data(ttl=600)
def get_precio_base_df(_client):
    # Load the base price data for products and rename columns for consistency
    df = load_precio_base(_client, SHEET_ID)
    df.columns = df.columns.str.strip()
    if "Codigo" in df.columns:
        df.rename(columns={"Codigo": "Codigo_Esparrago"}, inplace=True)
    return df

def recalculate_totals():
    """
    Recalculate the total amounts in the factura detail DataFrame stored in session state.
    This function ensures 'Cantidad' and 'Precio' are numeric and computes 'Total' as their product.
    It updates the session state with the recalculated DataFrame.
    """
    if "detalle_editor" in st.session_state:
        df = st.session_state["detalle_editor"]
        # Ensure df is a DataFrame and columns exist before referencing them
        if isinstance(df, pd.DataFrame) and "Cantidad" in df.columns and "Precio" in df.columns:
            # Convert 'Cantidad' and 'Precio' to numeric, coercing errors to 0.0
            df["Cantidad"] = pd.to_numeric(df["Cantidad"], errors="coerce").fillna(0.0)
            df["Precio"] = pd.to_numeric(df["Precio"], errors="coerce").fillna(0.0)
            # Calculate 'Total' as the product of 'Cantidad' and 'Precio'
            df["Total"] = df["Cantidad"] * df["Precio"]
            # Update session state with recalculated totals
            st.session_state["detalle_editor"] = df

def render(client, sheet_id, drive_service):
    """
    Render the Ingresar Facturas page with header and detalle forms together.
    This function handles user interaction for adding invoices, including:
    - Selecting action (Add/Edit/Delete), currently only Add is implemented.
    - Uploading invoice document files.
    - Inputting invoice header data (date, client, invoice number, observations).
    - Adding multiple product details with prices and quantities.
    - Calculating totals and displaying added products.
    - Saving the invoice header and details to Google Sheets.
    - Uploading the invoice document to Google Drive.
    """
    st.header("🧾 Gestión de Facturas")

    # Action selector: Add, Edit, or Delete invoices
    action = st.radio("Selecciona una acción:", ["Añadir", "Editar", "Eliminar"], horizontal=True)
    st.markdown("---")
    st.title("📄 Ingresar Factura")

    # Load supporting master data for clients and products
    clientes_df = get_clientes_df(client)
    productos_df = get_productos_df(client)

    # Prepare lists for selection widgets
    clientes_list = clientes_df["Nombre Cliente"].dropna().tolist()
    productos_list = productos_df["Codigo_Esparrago"].dropna().tolist()

    # Load product pricing table and prepare editable form
    precio_base_df = get_precio_base_df(client)

    # Initialize session state list to hold factura detail lines if not present
    if "factura_detalle_lines" not in st.session_state:
        st.session_state["factura_detalle_lines"] = []

    def get_precio_base(selected_producto):
        """
        Given a selected product code, return the base price from precio_base_df.
        Handles string cleaning and conversion to float.
        Returns 0.0 if product not found or conversion fails.
        """
        if selected_producto and selected_producto in precio_base_df["Codigo_Esparrago"].values:
            precio_base_row = precio_base_df[precio_base_df["Codigo_Esparrago"] == selected_producto]
            precio_str = precio_base_row["Precio"].values[0]
            try:
                return float(str(precio_str).replace("$", "").replace(",", "").strip())
            except ValueError:
                return 0.0
        return 0.0

    # Begin form for factura input
    with st.form("factura_form"):
        # File uploader to upload the invoice document (PDF, JPG, PNG)
        uploaded_file = st.file_uploader("Sube el documento de la factura", type=["pdf", "jpg", "png"])

        # Encabezado de Factura inputs
        # Capture the invoice date; defaults to today's date
        fecha = st.date_input("Fecha", value=datetime.today())
        # Select the client from the loaded list
        cliente = st.selectbox("Cliente", clientes_list)
        # Input field for the invoice number, mandatory for saving
        no_factura = st.text_input("Número de Factura")
        # Text area for any additional observations or notes
        observaciones = st.text_area("Observaciones")

        # Section for entering invoice detail lines (products)
        st.markdown("---")
        st.subheader("Detalles de Factura")
        st.markdown("**Ingresa las cantidades y modifica los precios si es necesario.**")

        # Layout columns for product detail inputs
        cols = st.columns([3, 2, 2, 2])
        with cols[0]:
            # Select product code from the product list
            selected_producto = st.selectbox("Producto", productos_list, key="new_producto")

        with cols[1]:
            # Retrieve base price for selected product; used as default price input
            precio_base = get_precio_base(selected_producto)
            # Numeric input for price, initialized with base price, allows modification
            precio = st.number_input("Precio", step=0.10, value=precio_base, key="new_precio_input")

        with cols[2]:
            # Numeric input for quantity, minimum 0, step 1
            cantidad = st.number_input("Cantidad", min_value=0, step=1, key="new_cantidad")

        with cols[3]:
            # Calculate total for this line as price * quantity
            total = precio * cantidad
            # Display the calculated total formatted as currency
            st.markdown(f"**Total: ${total:.2f}**")

        # Button to add the current product detail to the session state list
        if st.form_submit_button("Agregar Producto"):
            if cantidad > 0:
                # Append product detail line to session state list
                st.session_state.factura_detalle_lines.append({
                    "Codigo_Esparrago": selected_producto,
                    "Precio": precio,
                    "Cantidad": cantidad,
                    "Total": total
                })
                # Reset local variables after adding (not strictly necessary here)
                precio = precio_base
                cantidad = 0

        # Display the list of added products with their details and running total
        st.markdown("### Productos agregados:")
        total_factura = 0.0
        if st.session_state.factura_detalle_lines:
            for idx, item in enumerate(st.session_state.factura_detalle_lines):
                st.markdown(f"- {item['Codigo_Esparrago']} | Precio: ${item['Precio']:.2f} | Cantidad: {item['Cantidad']} | Total: ${item['Total']:.2f}")
                total_factura += item["Total"]
        else:
            st.markdown("No hay productos agregados aún.")

        # Button to submit and save the factura (header and details)
        submitted = st.form_submit_button("Guardar Factura")

    # Only 'Añadir' action is implemented; inform user otherwise
    if action != "Añadir":
        st.info("Solo la acción 'Añadir' está implementada actualmente.")
        return

    if submitted:
        # Validate that invoice number is provided
        if not no_factura:
            st.error("El número de factura es obligatorio.")
        # Validate that at least one product detail line is added
        elif len(st.session_state.factura_detalle_lines) == 0:
            st.error("Debe agregar al menos un detalle.")
        else:
            try:
                documento_url = ""
                # If a document file was uploaded, save it to Google Drive and get the URL
                if uploaded_file:
                    uploaded_info = save_uploaded_file_to_drive(uploaded_file, drive_service, FOLDER_ID_FACTURAS)
                    documento_url = uploaded_info.get("webViewLink", "")

                # Prepare the detalle DataFrame from session state list
                detalle_df_to_save = pd.DataFrame(st.session_state.factura_detalle_lines)
                detalle_df_to_save["No. Factura"] = no_factura
                # Calculate total invoice amount by summing 'Total' column
                total_factura = detalle_df_to_save["Total"].sum()
                # Identify user who is entering the data; default to 'Desconocido' if not set
                ingresado_por = st.session_state.get("user_email", "Desconocido")

                # Prepare header data dictionary to save
                header_data = {
                    "Fecha": fecha.strftime("%Y-%m-%d"),
                    "Semana": fecha.isocalendar()[1],
                    "No. Factura": no_factura,
                    "Cliente": cliente,
                    "Total": total_factura,
                    "DocumentoFactura": documento_url,
                    "Ingresado Por": ingresado_por,
                    "Fecha Ingresado": datetime.today().strftime("%Y-%m-%d"),
                    "Observaciones": observaciones,
                    "Procesado_Flag": False
                }

                # Save header and detail data to Google Sheets
                save_header_factura(client, INGRESAR_DATOS_SHEET_ID, header_data)
                save_detalle_facturas(client, INGRESAR_DATOS_SHEET_ID, detalle_df_to_save)

                # Inform user of success and clear the detail lines in session state
                st.success("Factura y detalles guardados correctamente.")
                st.session_state.factura_detalle_lines = []
            except Exception as e:
                # Handle any errors during save/upload and display error message
                st.error("Ocurrió un error al guardar la factura.")
                st.exception(e)
