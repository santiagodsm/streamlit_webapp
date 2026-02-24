import streamlit as st
import pandas as pd
from datetime import datetime
from utils.uploader import upload_file_to_folder
from utils.records import add_record
from utils.loaders import load_sheet_as_df
from config import FOLDER_ID_FACTURAS as INVOICE_FOLDER_ID

def render_header_factura_form(clientes_list, drive_service):
    """Render the form to capture HeaderFactura data."""
    with st.form("header_factura_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            fecha = st.date_input("Fecha")
            semana = fecha.isocalendar()[1]
            no_factura = st.text_input("No. Factura")
        with col2:
            cliente = st.selectbox("Cliente", clientes_list)
            total = st.number_input("Total", min_value=0.0, format="%.2f")
            documento_factura = st.file_uploader("Subir Documento de Factura", type=["pdf", "jpg", "png"])
        with col3:
            flete = st.number_input("Flete", min_value=0.0, format="%.2f")
            costo_aduanal = st.number_input("Costo Aduanal", min_value=0.0, format="%.2f")
            renta_bodega = st.number_input("Renta Bodega", min_value=0.0, format="%.2f")

        comision_dg = st.number_input("Comisión DG", min_value=0.0, format="%.2f")
        comision_broker = st.number_input("Comisión Broker", min_value=0.0, format="%.2f")
        total_final = st.number_input("Total Final", min_value=0.0, format="%.2f")
        observaciones = st.text_area("Observaciones")
        procesado_flag = st.checkbox("Procesado")

        submitted = st.form_submit_button("Guardar Factura")

        if submitted:
            documento_url = ""
            if documento_factura:
                documento_url = upload_file_to_folder(drive_service, INVOICE_FOLDER_ID, documento_factura)

            header_data = {
                "Fecha": fecha.strftime("%Y-%m-%d"),
                "Semana": semana,
                "No. Factura": no_factura,
                "Cliente": cliente,
                "Total": total,
                "DocumentoFactura": documento_url,
                "Flete": flete,
                "Costo Aduanal": costo_aduanal,
                "Renta Bodega": renta_bodega,
                "Comision DG": comision_dg,
                "Comision Broker": comision_broker,
                "Total Final": total_final,
                "Ingresado Por": st.session_state.get("user_email", "N/A"),
                "Fecha Ingresado": datetime.today().strftime("%Y-%m-%d"),
                "Observaciones": observaciones,
                "Procesado_Flag": procesado_flag
            }
            return header_data
    return None

def render_detalle_factura_form(productos_list, no_factura_selected):
    """Render the form to capture DetalleFactura data."""
    with st.form("detalle_factura_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            codigo_esparrago = st.selectbox("Código Espárrago", productos_list)
            cantidad = st.number_input("Cantidad", min_value=0.0, format="%.2f")
        with col2:
            precio = st.number_input("Precio", min_value=0.0, format="%.2f")
            precio_venta_agricultor = st.number_input("Precio Venta Agricultor", min_value=0.0, format="%.2f")
        with col3:
            precio_venta = st.number_input("Precio Venta", min_value=0.0, format="%.2f")

        procesado = st.checkbox("Procesado")

        submitted = st.form_submit_button("Agregar Detalle")

        if submitted:
            total = cantidad * precio
            total_final = cantidad * precio_venta

            detalle_data = {
                "No. Factura": no_factura_selected,
                "Codigo_Esparrago": codigo_esparrago,
                "Cantidad": cantidad,
                "Precio": precio,
                "Total": total,
                "Precio de Venta Agricultor": precio_venta_agricultor,
                "Precio de Venta": precio_venta,
                "Total Final": total_final,
                "Procesado": procesado
            }
            return detalle_data
    return None

def save_uploaded_file_to_drive(uploaded_file, drive_service, folder_id):
    """Uploads a Streamlit uploaded file to Google Drive and returns the file metadata."""
    if uploaded_file is None:
        return {}

    upload_result = upload_file_to_folder(drive_service, folder_id, uploaded_file)
    return upload_result

def save_header_factura(client, sheet_id, header_data):
    """Saves the header factura information to the 'HeaderFactura' worksheet."""
    ws = client.open_by_key(sheet_id).worksheet("HeaderFactura")
    df = pd.DataFrame(ws.get_all_records())
    add_record(df, ws, header_data, key_col="No. Factura")

def load_precio_base(client, sheet_id):
    """
    Loads base price data from Producto_Esparrago sheet.
    Returns a DataFrame with Codigo and Precio columns.
    """
    df = load_sheet_as_df(client, sheet_id, "Producto_Esparrago")
    return df[["Codigo_Esparrago", "Precio Factura Base"]].rename(columns={
        "Codigo_Esparrago": "Codigo",
        "Precio Factura Base": "Precio"
    })

def prepare_detalle_input_table(base_df):
    """
    Adds editable Cantidad and computed Total columns to the base product price DataFrame.
    """
    base_df["Cantidad"] = 0.0
    base_df["Total"] = 0.0
    return base_df

def save_detalle_facturas(client, sheet_id, df_detalles):
    """
    Saves detalle factura entries from a DataFrame to the DetalleFactura worksheet.
    Only rows where Cantidad > 0 are saved.
    """
    ws = client.open_by_key(sheet_id).worksheet("DetalleFactura")
    existing_df = pd.DataFrame(ws.get_all_records())
    filtered = df_detalles[df_detalles["Cantidad"] > 0.0].copy()
    for _, row in filtered.iterrows():
        record = {
            "No. Factura": row["No. Factura"],
            "Codigo_Esparrago": row["Codigo"],
            "Cantidad": row["Cantidad"],
            "Precio": row["Precio"],
            "Total": row["Cantidad"] * row["Precio"],
            "Precio de Venta Agricultor": "",
            "Precio de Venta": "",
            "Total Final": "",
            "Procesado": False
        }
        add_record(existing_df, ws, record, key_col=None)
