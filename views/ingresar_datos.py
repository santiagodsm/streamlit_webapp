import streamlit as st
import views.ingresar_datos.facturas as facturas
import views.ingresar_datos.folios as folios

def render(client, sheet_id, drive_service):
    """
    Landing page for Ingresar Datos section.
    Provides navigation between Ingresar Facturas and Ingresar Folios.
    """

    st.title("📝 Ingresar Datos")

    st.markdown("---")
    st.subheader("Selecciona qué deseas ingresar:")

    option = st.radio(
        "",
        ["📄 Ingresar Factura", "📦 Ingresar Folio"],
        horizontal=True
    )

    if option == "📄 Ingresar Factura":
        facturas.render(client, sheet_id, drive_service)
    elif option == "📦 Ingresar Folio":
        folios.render(client, sheet_id, drive_service)