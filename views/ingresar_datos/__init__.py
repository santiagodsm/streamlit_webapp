

import streamlit as st
from views.ingresar_datos import facturas, folios

def render(client, sheet_id, drive_service):
    """Render the Ingresar Datos main page with navigation to Facturas or Folios."""
    st.title("📝 Ingresar Datos")

    section = st.radio(
        "¿Qué deseas ingresar?",
        ["Facturas", "Folios"],
        horizontal=True
    )

    if section == "Facturas":
        facturas.render(client, sheet_id, drive_service)
    elif section == "Folios":
        folios.render(client, sheet_id, drive_service)