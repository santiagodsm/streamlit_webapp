# =========================================================
# Gestión de Productos Espárrago
# - Permite visualizar, añadir, editar y eliminar productos
# - Valida campos obligatorios y formatos de tipo moneda/número
# =========================================================

import streamlit as st
import pandas as pd
from utils.loaders import load_sheet_as_df
from utils.records import add_record, edit_record, delete_record_by_key
from utils.validators import is_currency, is_numeric, is_required, is_unique
from utils.forms import build_producto_esparrago_form

def render(client, sheet_id):
    """Renderiza la interfaz de gestión de productos de espárrago."""

    sheet_name = "Producto_Esparrago"

    # Cargar los datos desde la hoja de Google Sheets
    df = load_sheet_as_df(client, sheet_id, sheet_name)

    if df is None or df.empty:
        st.error("No se pudieron cargar los datos de productos. Revisa la conexión con la hoja o si hay datos disponibles.")
        return

    # Mostrar la tabla de productos
    
    st.dataframe(df)

    st.markdown("---")
    st.subheader("🛠️ Opciones de Gestión")

    # Seleccionar acción: Editar, Añadir o Eliminar
    action = st.radio("Selecciona una acción:", ["Editar", "Añadir", "Eliminar"], horizontal=True)

    # Obtener la hoja de trabajo
    ws = client.open_by_key(sheet_id).worksheet(sheet_name)

    if action == "Editar":
        # --- Sección para Editar Producto ---
        codigos = df["Codigo_Esparrago"].unique()
        selected_codigo = st.selectbox("Selecciona el Código a modificar:", codigos)
        current = df[df["Codigo_Esparrago"] == selected_codigo].iloc[0].to_dict()

        with st.form("edit_producto_form"):
            (codigo, nombre, tipo_caja, primeras_segundas, cajas,
            avance, costo_cajas, precio_factura, avance_cajas, avance_empaque, multiplicativo) = build_producto_esparrago_form(current)
            submitted = st.form_submit_button("Guardar Cambios")

        if submitted:
            errors = []
            # Validar campos obligatorios
            if not all(map(is_required, [codigo, nombre, tipo_caja, primeras_segundas, cajas])):
                errors.append("Todos los campos de texto son obligatorios.")
            # Validar campos monetarios y formatear
            currency_fields = [avance, costo_cajas, precio_factura, avance_cajas, avance_empaque]
            formatted_fields = []
            all_valid = True

            for field in currency_fields:
                try:
                    field_clean = str(field).replace("$", "").replace(",", "").strip()
                    num = float(field_clean)
                    formatted_fields.append(f"${num:.2f}")
                except (ValueError, TypeError):
                    all_valid = False
                    errors.append("Todos los campos monetarios deben ser numéricos válidos.")
                    break

            if all_valid:
                avance, costo_cajas, precio_factura, avance_cajas, avance_empaque = formatted_fields
            # Validar campo numérico
            if not is_numeric(multiplicativo):
                errors.append("Multiplicativo debe ser numérico.")

            # Mostrar errores o actualizar registro
            if errors:
                for e in errors:
                    st.error(e)
            else:
                updated_dict = {
                    "Codigo_Esparrago": codigo.strip(),
                    "Nombre": nombre.strip(),
                    "TipoCaja": tipo_caja,
                    "Primeras/Segundas": primeras_segundas,
                    "Cajas": cajas,
                    "Avance": avance.strip(),
                    "Costo Cajas": costo_cajas.strip(),
                    "Precio Factura Base": precio_factura.strip(),
                    "Avance Cajas": avance_cajas.strip(),
                    "Avance Empaque": avance_empaque.strip(),
                    "Multiplicativo": multiplicativo.strip()
                }
                try:
                    edit_record(df, ws, "Codigo_Esparrago", selected_codigo, updated_dict)
                    st.success("Producto actualizado correctamente.")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))

    elif action == "Añadir":
        # --- Sección para Añadir Producto ---
        with st.form("add_producto_form"):
            (codigo, nombre, tipo_caja, primeras_segundas, cajas,
            avance, costo_cajas, precio_factura, avance_cajas, avance_empaque, multiplicativo) = build_producto_esparrago_form()
            submitted = st.form_submit_button("Añadir Producto")

        if submitted:
            errors = []
            # Validar campos obligatorios
            if not all(map(is_required, [codigo, nombre, tipo_caja, primeras_segundas, cajas])):
                errors.append("Todos los campos de texto son obligatorios.")
            # Validar unicidad del Código Esparrago
            if not is_unique(df, "Codigo_Esparrago", codigo):
                errors.append("Código Esparrago ya existe.")
            # Validar campos monetarios y formatear
            currency_fields = [avance, costo_cajas, precio_factura, avance_cajas, avance_empaque]
            formatted_fields = []
            all_valid = True

            for field in currency_fields:
                try:
                    field_clean = str(field).replace("$", "").replace(",", "").strip()
                    num = float(field_clean)
                    formatted_fields.append(f"${num:.2f}")
                except (ValueError, TypeError):
                    all_valid = False
                    errors.append("Todos los campos monetarios deben ser numéricos válidos.")
                    break

            if all_valid:
                avance, costo_cajas, precio_factura, avance_cajas, avance_empaque = formatted_fields
            # Validar campo numérico
            if not is_numeric(multiplicativo):
                errors.append("Multiplicativo debe ser numérico.")

            # Mostrar errores o agregar nuevo registro
            if errors:
                for e in errors:
                    st.error(e)
            else:
                new_row = {
                    "Codigo_Esparrago": codigo.strip(),
                    "Nombre": nombre.strip(),
                    "TipoCaja": tipo_caja,
                    "Primeras/Segundas": primeras_segundas,
                    "Cajas": cajas,
                    "Avance": avance.strip(),
                    "Costo Cajas": costo_cajas.strip(),
                    "Precio Factura Base": precio_factura.strip(),
                    "Avance Cajas": avance_cajas.strip(),
                    "Avance Empaque": avance_empaque.strip(),
                    "Multiplicativo": multiplicativo.strip()
                }
                try:
                    add_record(df, ws, new_row, "Codigo_Esparrago")
                    st.success("Producto añadido correctamente.")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))

    elif action == "Eliminar":
        # --- Sección para Eliminar Producto ---
        codigos = df["Codigo_Esparrago"].unique()
        selected_codigo_del = st.selectbox("Selecciona el Código del producto a eliminar:", codigos)
        confirm_text = st.text_input("Escribe 'delete' para confirmar la eliminación")
        if st.button("Eliminar producto"):
            if confirm_text.lower() == 'delete':
                try:
                    delete_record_by_key(df, ws, "Codigo_Esparrago", selected_codigo_del)
                    st.success("Producto eliminado correctamente.")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))
            else:
                st.warning("Debes escribir 'delete' para confirmar.")