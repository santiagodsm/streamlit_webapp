# =========================================================
# Cajas Page
# - Allows users to view, add, edit, and delete cajas records
# - Auto-calculates the 'Totales' field based on currency fields
# =========================================================

import streamlit as st
from utils.loaders import load_sheet_as_df
from utils.forms import build_caja_form, confirm_deletion
from utils.records import add_record, edit_record, delete_record_by_key
from utils.validators import is_required, is_currency, is_numeric, is_unique

def render(client, sheet_id):
    """
    Render the Cajas management page.

    Args:
        client: Authorized gspread client instance.
        sheet_id (str): Google Sheet ID.
    """

    sheet_name = "Cajas"

    # --- Load existing Cajas data ---
    df = load_sheet_as_df(client, sheet_id, sheet_name)

    # Display the current Cajas in a DataFrame
    st.dataframe(df)

    st.markdown("---")
    st.subheader("🛠️ Opciones de Gestión")

    # --- Radio selection for actions ---
    action = st.radio("Selecciona una acción:", ["Editar", "Añadir", "Eliminar"], horizontal=True)

    ws = client.open_by_key(sheet_id).worksheet(sheet_name)

    if action == "Editar":
        # ==========================
        # Edit an existing Caja
        # ==========================
        conceptos = df["Concepto"].unique()
        selected_concepto = st.selectbox("Selecciona el Concepto a editar:", conceptos)
        current = df[df["Concepto"] == selected_concepto].iloc[0].to_dict()

        with st.form("edit_caja_form"):
            form_data = build_caja_form(current)
            submitted = st.form_submit_button("Guardar Cambios")

            if submitted:
                concepto, multiplicativo, caja, panal, liga, flete_importa, sueldos, renta, ryan, empaque, tags_bags, flete_locales = form_data

                fields = [caja, panal, liga, flete_importa, sueldos, renta, ryan, empaque, tags_bags, flete_locales]

                if not is_required(concepto) or not is_numeric(multiplicativo):
                    st.error("Concepto es obligatorio y Multiplicativo debe ser numérico.")
                else:
                    formatted_fields = []
                    all_valid = True

                    for field in fields:
                        try:
                            field_clean = str(field).replace("$", "").replace(",", "").strip()
                            num = float(field_clean)
                            formatted_fields.append(f"${num:.2f}")
                        except (ValueError, TypeError):
                            all_valid = False
                            st.error(f"El campo '{field}' no es válido. Debe ser numérico.")

                    if not all_valid:
                        st.stop()

                    (
                        caja, panal, liga, flete_importa,
                        sueldos, renta, ryan, empaque,
                        tags_bags, flete_locales
                    ) = formatted_fields

                    # Calculate Totales
                    total = sum(float(f.replace("$", "").replace(",", "")) for f in formatted_fields)
                    updated_dict = {
                        "Concepto": concepto.strip(),
                        "Multiplicativo": multiplicativo.strip(),
                        "Caja": caja.strip(),
                        "Panal": panal.strip(),
                        "Liga": liga.strip(),
                        "Flete Importa": flete_importa.strip(),
                        "Sueldos": sueldos.strip(),
                        "Renta": renta.strip(),
                        "Ryan": ryan.strip(),
                        "Empaque": empaque.strip(),
                        "Tags/Bags": tags_bags.strip(),
                        "Flete Locales": flete_locales.strip(),
                        "Totales": str(total)
                    }
                    edit_record(df, ws, "Concepto", selected_concepto, updated_dict)
                    st.success("Registro actualizado correctamente.")
                    st.rerun()

    elif action == "Añadir":
        # ==========================
        # Add a new Caja
        # ==========================
        with st.form("add_caja_form"):
            form_data = build_caja_form()
            submitted = st.form_submit_button("Agregar Caja")

            if submitted:
                concepto, multiplicativo, caja, panal, liga, flete_importa, sueldos, renta, ryan, empaque, tags_bags, flete_locales = form_data

                fields = [caja, panal, liga, flete_importa, sueldos, renta, ryan, empaque, tags_bags, flete_locales]

                if not is_required(concepto) or not is_numeric(multiplicativo):
                    st.error("Concepto es obligatorio y Multiplicativo debe ser numérico.")
                elif not is_unique(df, "Concepto", concepto.strip()):
                    st.error("El concepto ya existe. Debe ser único.")
                else:
                    formatted_fields = []
                    all_valid = True

                    for field in fields:
                        try:
                            field_clean = str(field).replace("$", "").replace(",", "").strip()
                            num = float(field_clean)
                            formatted_fields.append(f"${num:.2f}")
                        except (ValueError, TypeError):
                            all_valid = False
                            st.error(f"El campo '{field}' no es válido. Debe ser numérico.")

                    if not all_valid:
                        st.stop()

                    (
                        caja, panal, liga, flete_importa,
                        sueldos, renta, ryan, empaque,
                        tags_bags, flete_locales
                    ) = formatted_fields

                    # Calculate Totales
                    total = sum(float(f.replace("$", "").replace(",", "")) for f in formatted_fields)
                    new_row_dict = {
                        "Concepto": concepto.strip(),
                        "Multiplicativo": multiplicativo.strip(),
                        "Caja": caja.strip(),
                        "Panal": panal.strip(),
                        "Liga": liga.strip(),
                        "Flete Importa": flete_importa.strip(),
                        "Sueldos": sueldos.strip(),
                        "Renta": renta.strip(),
                        "Ryan": ryan.strip(),
                        "Empaque": empaque.strip(),
                        "Tags/Bags": tags_bags.strip(),
                        "Flete Locales": flete_locales.strip(),
                        "Totales": str(total)
                    }
                    add_record(df, ws, new_row_dict, "Concepto")
                    st.success("Nueva caja agregada correctamente.")
                    st.rerun()

    elif action == "Eliminar":
        # ==========================
        # Delete an existing Caja
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