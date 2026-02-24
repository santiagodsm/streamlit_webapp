# =========================================================
# Gestión de Clientes
# - Permite visualizar, añadir, editar y eliminar clientes
# - Permite subir un logo de cliente a Google Drive
# - Actualiza las hojas de Google Sheets dinámicamente
# =========================================================

from utils.loaders import load_sheet_as_df
from utils.records import add_record, edit_record, delete_record_by_key
from utils.validators import is_valid_phone, is_required, is_unique
from utils.forms import build_cliente_form, build_cliente_add_form, confirm_cliente_deletion
from utils.auth import get_drive_service
from utils.uploader import upload_file_to_drive
from config import FOLDER_ID_CLIENTES_LOGOS
import pandas as pd
import streamlit as st

def render(client, sheet_id, drive_service):
    """Renderiza la gestión de clientes."""

    # --- Cargar datos de la hoja "Clientes" ---
    df = load_sheet_as_df(client, sheet_id, "Clientes")

    # Mostrar los clientes actuales
    st.dataframe(df)

    st.markdown("---")
    st.subheader("🛠️ Opciones de Gestión")

    # --- Seleccionar acción: Editar, Añadir o Eliminar ---
    action = st.radio("Selecciona una acción:", ["Editar", "Añadir", "Eliminar"], horizontal=True)

    if action == "Editar":
        # ===============================
        # Sección para editar un cliente
        # ===============================
        st.subheader("Editar Cliente")
        col1, col2 = st.columns(2)

        with col1:
            # Selección del ID del cliente a editar
            selected_id = st.selectbox("Seleccione ID del cliente a editar", df['ID'])

        # Obtener datos actuales del cliente
        cliente_row = df[df['ID'] == selected_id].iloc[0]

        with col2:
            # Construir formulario de edición
            nombre, telefono, icono, direccion = build_cliente_form(cliente_row)

            # Subir nuevo logo si aplica
            uploaded_file = st.file_uploader("Subir logo del cliente", type=["jpg", "png", "jpeg"])
            icon_url = ""
            if uploaded_file:
                import tempfile
                temp_file = tempfile.NamedTemporaryFile(delete=False)
                temp_file.write(uploaded_file.read())
                temp_file.close()

                uploaded_file_id = upload_file_to_drive(
                    drive_service,
                    temp_file.name,
                    FOLDER_ID_CLIENTES_LOGOS,
                    uploaded_file.name
                )
                icon_url = f"https://drive.google.com/uc?export=view&id={uploaded_file_id}"

            # Previsualizar logo si fue cargado
            if icon_url:
                st.markdown(f'<img src="{icon_url}" width="100" alt="Vista previa del logo">', unsafe_allow_html=True)

        if st.button("Guardar cambios"):
            # Validaciones
            if icon_url:
                icono = icon_url
            if not is_required(nombre):
                st.error("Nombre Cliente es obligatorio")
            elif telefono and not is_valid_phone(telefono):
                st.error("Telefono debe contener solo números")
            else:
                # Actualizar cliente
                updated_dict = {
                    'ID': selected_id,
                    'Nombre Cliente': nombre.strip(),
                    'Telefono': telefono.strip(),
                    'Icono': icon_url if icon_url else icono.strip(),
                    'Dirección': direccion.strip()
                }
                try:
                    edit_record(df, client.open_by_key(sheet_id).worksheet("Clientes"), "ID", selected_id, updated_dict)
                    st.success("Cliente actualizado correctamente")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))

    elif action == "Añadir":
        # ===============================
        # Sección para añadir un cliente
        # ===============================
        st.subheader("Añadir Cliente")

        # Formulario para nuevo cliente
        new_id, new_nombre, new_telefono, new_icono = build_cliente_add_form()

        uploaded_file = st.file_uploader("Subir logo del cliente", type=["jpg", "png", "jpeg"])
        icon_url = ""
        if uploaded_file:
            import tempfile
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_file.write(uploaded_file.read())
            temp_file.close()

            uploaded_file_id = upload_file_to_drive(
                drive_service,
                temp_file.name,
                FOLDER_ID_CLIENTES_LOGOS,
                uploaded_file.name
            )
            icon_url = f"https://drive.google.com/uc?export=view&id={uploaded_file_id}"

        if icon_url:
            st.markdown(f'<img src="{icon_url}" width="100" alt="Vista previa del logo">', unsafe_allow_html=True)

        if st.button("Añadir cliente"):
            # Validaciones
            if icon_url:
                new_icono = icon_url
            if not is_required(new_id):
                st.error("ID es obligatorio")
            elif not is_required(new_nombre):
                st.error("Nombre Cliente es obligatorio")
            elif new_telefono and not is_valid_phone(new_telefono):
                st.error("Telefono debe contener solo números")
            elif not is_unique(df, "ID", new_id):
                st.error("ID ya existe")
            else:
                # Insertar nuevo cliente
                new_row = {
                    'ID': int(new_id.strip()),
                    'Nombre Cliente': new_nombre.strip(),
                    'Telefono': new_telefono.strip(),
                    'Icono': icon_url if icon_url else new_icono.strip(),
                    'Dirección': ""
                }
                try:
                    add_record(df, client.open_by_key(sheet_id).worksheet("Clientes"), new_row, "ID")
                    st.success("Cliente añadido correctamente")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))

    elif action == "Eliminar":
        # ===============================
        # Sección para eliminar un cliente
        # ===============================
        st.subheader("Eliminar Cliente")

        # Selección de ID de cliente a eliminar
        selected_id_del = st.selectbox("Seleccione ID del cliente a eliminar", df['ID'])

        # Confirmación de eliminación
        if confirm_cliente_deletion():
            try:
                delete_record_by_key(df, client.open_by_key(sheet_id).worksheet("Clientes"), "ID", selected_id_del)
                st.success("Cliente eliminado correctamente")
                st.rerun()
            except Exception as e:
                st.error(str(e))
