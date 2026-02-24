# =========================================================
# Gestión de Agricultores
# - Permite visualizar, añadir, editar y eliminar agricultores
# - Valida correos electrónicos, teléfonos y unicidad de claves
# =========================================================

import streamlit as st
import pandas as pd
from utils.loaders import load_sheet_as_df
from utils.writers import append_row_to_sheet
import re
from utils.records import add_record, edit_record, delete_record_by_key
from utils.validators import is_valid_email, is_valid_phone, is_unique, is_required
from utils.forms import build_agricultor_form, confirm_deletion

def render(client, sheet_id):
    """Renderiza la gestión de agricultores."""

    sheet_name = "Agricultores"

    # --- Cargar datos de agricultores desde la hoja ---
    df = load_sheet_as_df(client, sheet_id, sheet_name)

    # Mostrar los datos en un dataframe
    st.dataframe(df)

    st.markdown("---")
    st.subheader("🛠️ Opciones de Gestión")

    # --- Seleccionar acción: Editar, Añadir o Eliminar ---
    action = st.radio("Selecciona una acción:", ["Editar", "Añadir", "Eliminar"], horizontal=True)

    # Obtener referencia a la hoja de Google Sheets
    ws = client.open_by_key(sheet_id).worksheet(sheet_name)

    if action == "Editar":
        # ==========================
        # Sección para editar registro
        # ==========================
        claves = df["Clave"].unique()
        selected_clave = st.selectbox("Selecciona la Clave del agricultor a modificar:", claves)
        current = df[df["Clave"] == selected_clave].iloc[0].to_dict()

        with st.form("edit_form"):
            # Construir formulario para edición
            agricultor, zona, email, telefono, direccion = build_agricultor_form(current)
            submitted = st.form_submit_button("Guardar Cambios")

            email_valid = True
            telefono_valid = True

            # Validar email
            if email and not is_valid_email(email):
                st.error("El correo electrónico no es válido.")
                email_valid = False

            # Validar teléfono
            if telefono and not is_valid_phone(telefono):
                st.error("El teléfono no es válido.")
                telefono_valid = False

            if submitted:
                if not email_valid or not telefono_valid:
                    st.warning("Corrige los errores antes de continuar.")
                elif is_required(agricultor):
                    # Preparar registro actualizado
                    updated_dict = {
                        "Clave": selected_clave,
                        "Agricultor": agricultor,
                        "Zona": zona,
                        "Email": email,
                        "Telefono": telefono,
                        "Direccion": direccion,
                        "Orden": current.get("Orden", "")
                    }
                    # Actualizar en la hoja
                    edit_record(df, ws, "Clave", selected_clave, updated_dict)
                    st.success("Registro actualizado correctamente.")
                    st.rerun()
                else:
                    st.error("El campo 'Agricultor' es obligatorio.")

    elif action == "Añadir":
        # ==========================
        # Sección para añadir nuevo agricultor
        # ==========================
        with st.form("add_form"):
            clave = st.text_input("Clave")
            agricultor, zona, email, telefono, direccion = build_agricultor_form()
            submitted = st.form_submit_button("Agregar Agricultor")

            email_valid = True
            telefono_valid = True

            # Validar email
            if email and not is_valid_email(email):
                st.error("El correo electrónico no es válido.")
                email_valid = False

            # Validar teléfono
            if telefono and not is_valid_phone(telefono):
                st.error("El teléfono no es válido.")
                telefono_valid = False

            if submitted:
                if not email_valid or not telefono_valid:
                    st.warning("Corrige los errores antes de continuar.")
                elif not (is_required(clave) and is_required(agricultor)):
                    st.error("Los campos 'Clave' y 'Agricultor' son obligatorios.")
                elif not is_unique(df, "Clave", clave):
                    st.error("La clave ya existe. Debe ser única.")
                else:
                    # Preparar nuevo registro
                    new_row_dict = {
                        "Clave": clave,
                        "Agricultor": agricultor,
                        "Zona": zona,
                        "Email": email,
                        "Telefono": telefono,
                        "Direccion": direccion,
                        "Orden": ""
                    }
                    # Agregar a la hoja
                    add_record(df, ws, new_row_dict, "Clave")
                    st.success("Nuevo agricultor agregado correctamente.")
                    st.rerun()

    elif action == "Eliminar":
        # ==========================
        # Sección para eliminar agricultor
        # ==========================
        claves = df["Clave"].unique()
        selected_clave = st.selectbox("Selecciona la Clave del agricultor a eliminar:", claves)

        if st.button("Eliminar"):
            if confirm_deletion():
                try:
                    delete_record_by_key(df, ws, "Clave", selected_clave)
                    st.success("Registro eliminado correctamente.")
                    st.rerun()
                except Exception as e:
                    st.error("No se pudo eliminar el registro.")
                    st.exception(e)
            else:
                st.warning("Debes escribir 'delete' para confirmar la eliminación.")