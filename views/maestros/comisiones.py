# =========================================================
# Comisiones Page
# - Allows users to view, add, edit, and delete comisiones records
# - Each record has a Concepto (ID) and a Porcentaje (percentage)
# - Validations ensure required fields, uniqueness, and numeric correctness
# =========================================================

import streamlit as st
from utils.loaders import load_sheet_as_df
from utils.forms import build_comision_form, confirm_deletion
from utils.records import add_record, edit_record, delete_record_by_key
from utils.validators import is_required, is_numeric, is_unique

def render(client, sheet_id):
    """
    Render the Comisiones management page.

    Args:
        client: Authorized gspread client instance.
        sheet_id (str): Google Sheet ID.
    """

    sheet_name = "Comisiones"

    # --- Load existing comisiones data ---
    df = load_sheet_as_df(client, sheet_id, sheet_name)

    # Display the current Comisiones in a DataFrame
    st.dataframe(df)

    st.markdown("---")
    st.subheader("🛠️ Opciones de Gestión")

    # --- Radio selection for actions ---
    action = st.radio("Selecciona una acción:", ["Editar", "Añadir", "Eliminar"], horizontal=True)

    ws = client.open_by_key(sheet_id).worksheet(sheet_name)

    if action == "Editar":
        # ==========================
        # Edit an existing Comision
        # ==========================
        conceptos = df["Concepto"].unique()
        selected_concepto = st.selectbox("Selecciona el Concepto a editar:", conceptos)
        current = df[df["Concepto"] == selected_concepto].iloc[0].to_dict()

        with st.form("edit_comision_form"):
            concepto, porcentaje = build_comision_form(current)
            submitted = st.form_submit_button("Guardar Cambios")

            porcentaje_valid = is_numeric(porcentaje)

            if submitted:
                if not is_required(concepto):
                    st.error("El campo 'Concepto' es obligatorio.")
                elif not porcentaje_valid:
                    st.error("Porcentaje debe ser un número válido.")
                else:
                    try:
                        porcentaje_clean = str(porcentaje).replace("%", "").replace(",", "").strip()
                        porcentaje_formatted = f"{float(porcentaje_clean):.2f}%"
                        updated_dict = {
                            "Concepto": concepto.strip(),
                            "Porcentaje": porcentaje_formatted
                        }
                        edit_record(df, ws, "Concepto", selected_concepto, updated_dict)
                        st.success("Registro actualizado correctamente.")
                        st.rerun()
                    except ValueError:
                        st.error("Porcentaje debe ser un número válido.")
                        st.stop()

    elif action == "Añadir":
        # ==========================
        # Add a new Comision
        # ==========================
        with st.form("add_comision_form"):
            concepto, porcentaje = build_comision_form()
            submitted = st.form_submit_button("Agregar Comisión")

            porcentaje_valid = is_numeric(porcentaje)

            if submitted:
                if not is_required(concepto) or not is_required(porcentaje):
                    st.error("Los campos 'Concepto' y 'Porcentaje' son obligatorios.")
                elif not porcentaje_valid:
                    st.error("Porcentaje debe ser un número válido.")
                elif not is_unique(df, "Concepto", concepto.strip()):
                    st.error("El concepto ya existe. Debe ser único.")
                else:
                    try:
                        porcentaje_clean = str(porcentaje).replace("%", "").replace(",", "").strip()
                        porcentaje_formatted = f"{float(porcentaje_clean):.2f}%"
                        new_row_dict = {
                            "Concepto": concepto.strip(),
                            "Porcentaje": porcentaje_formatted
                        }
                        add_record(df, ws, new_row_dict, "Concepto")
                        st.success("Nueva comisión agregada correctamente.")
                        st.rerun()
                    except ValueError:
                        st.error("Porcentaje debe ser un número válido.")
                        st.stop()

    elif action == "Eliminar":
        # ==========================
        # Delete an existing Comision
        # ==========================
        conceptos = df["Concepto"].unique()
        selected_concepto = st.selectbox("Selecciona el Concepto a eliminar:", conceptos)

        if st.button("Eliminar"):
            if confirm_deletion():
                try:
                    delete_record_by_key(df, ws, "Concepto", selected_concepto)
                    st.success("Registro eliminado correctamente.")
                    st.rerun()
                except Exception as e:
                    st.error("No se pudo eliminar el registro.")
                    st.exception(e)
            else:
                st.warning("Debes escribir 'delete' para confirmar la eliminación.")