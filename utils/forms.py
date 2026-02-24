# =========================================================
# Forms Utility
# - Builds Streamlit form layouts for different modules
# - Used to structure form input fields for Agricultores, Clientes, and Producto Esparrago
# =========================================================

import streamlit as st

def build_agricultor_form(current_data=None):
    """
    Create the form layout for editing or adding an Agricultor.

    Args:
        current_data (dict, optional): Existing data to pre-fill the form (for editing).

    Returns:
        Tuple of str: Agricultor, Zona, Email, Telefono, Direccion fields.
    """
    col1, col2, col3 = st.columns(3)
    with col1:
        agricultor = st.text_input("Agricultor", value=current_data.get("Agricultor", "") if current_data else "")
    with col2:
        zona = st.text_input("Zona", value=current_data.get("Zona", "") if current_data else "")
    with col3:
        email = st.text_input("Email", value=current_data.get("Email", "") if current_data else "")
    
    col4, col5 = st.columns(2)
    with col4:
        telefono = st.text_input("Teléfono", value=current_data.get("Telefono", "") if current_data else "")
    with col5:
        direccion = st.text_input("Dirección", value=current_data.get("Direccion", "") if current_data else "")

    return agricultor, zona, email, telefono, direccion

def confirm_deletion():
    """
    Display a confirmation input for deletion, requiring user to type 'delete'.

    Returns:
        bool: True if confirmed, False otherwise.
    """
    confirmation = st.text_input("Escribe 'delete' para confirmar la eliminación:")
    return confirmation.lower() == "delete"

def build_cliente_form(current_data=None):
    """
    Create the form layout for editing an existing Cliente.

    Args:
        current_data (dict or pd.Series, optional): Existing data to pre-fill the form.

    Returns:
        Tuple of str: Nombre Cliente, Telefono, Icono URL, Direccion fields.
    """
    # Ensure compatibility if input is a Series
    current_data = current_data.to_dict() if hasattr(current_data, "to_dict") else current_data
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre Cliente", value=current_data.get("Nombre Cliente", "") if current_data else "")
        telefono = st.text_input("Telefono", value=current_data.get("Telefono", "") if current_data else "")
    with col2:
        icono = st.text_input("Icono URL", value=current_data.get("Icono", "") if current_data else "")
        direccion = st.text_input("Dirección", value=current_data.get("Direccion", "") if current_data else "")
    
    # Preview icon image if available
    if icono:
        st.image(icono, width=40)

    return nombre, telefono, icono, direccion

def build_cliente_add_form():
    """
    Create the form layout for adding a new Cliente.

    Returns:
        Tuple of str: ID, Nombre Cliente, Telefono, Icono URL fields.
    """
    col1, col2 = st.columns(2)
    with col1:
        new_id = st.text_input("ID")
        new_nombre = st.text_input("Nombre Cliente")
    with col2:
        new_telefono = st.text_input("Telefono")
        new_icono = st.text_input("Icono URL")
    
    # Preview uploaded icon if URL provided
    if new_icono:
        st.image(new_icono, width=40)

    return new_id, new_nombre, new_telefono, new_icono

def confirm_cliente_deletion():
    """
    Display a confirmation input specifically for deleting a Cliente.

    Returns:
        bool: True if user typed 'delete', False otherwise.
    """
    confirmation = st.text_input("Escriba 'delete' para confirmar la eliminación")
    return confirmation.lower() == "delete"

def build_producto_esparrago_form(current_data=None):
    """
    Create the form layout for Producto Esparrago management.

    Args:
        current_data (dict, optional): Existing data to pre-fill the form.

    Returns:
        Tuple of str: Fields related to Producto Esparrago (e.g., Código, Nombre, etc.)
    """
    tipo_caja_options = ["Made+Cart", "Fresh 28", "Costco 28", "Costco 36", "Cajas Segunda 28"]
    primeras_segundas_options = ["Primeras", "Segundas"]
    cajas_options = ["11 Lbs", "Walmart", "28 Lbs", "Costco", "36 Lbs", "Small 28", "Tips"]

    col1, col2, col3 = st.columns(3)
    with col1:
        codigo = st.text_input("Código Esparrago", value=current_data.get("Codigo_Esparrago", "") if current_data else "")
        nombre = st.text_input("Nombre", value=current_data.get("Nombre", "") if current_data else "")
        tipo_caja = st.selectbox(
            "Tipo de Caja",
            tipo_caja_options,
            index=tipo_caja_options.index(current_data.get("TipoCaja", tipo_caja_options[0])) if current_data else 0
        )
    with col2:
        primeras_segundas = st.selectbox(
            "Primeras/Segundas",
            primeras_segundas_options,
            index=primeras_segundas_options.index(current_data.get("Primeras/Segundas", primeras_segundas_options[0])) if current_data else 0
        )
        cajas = st.selectbox(
            "Cajas",
            cajas_options,
            index=cajas_options.index(current_data.get("Cajas", cajas_options[0])) if current_data else 0
        )
        avance = st.text_input("Avance", value=current_data.get("Avance", "") if current_data else "")
    with col3:
        costo_cajas = st.text_input("Costo Cajas", value=current_data.get("Costo Cajas", "") if current_data else "")
        precio_factura = st.text_input("Precio Factura Base", value=current_data.get("Precio Factura Base", "") if current_data else "")
        avance_cajas = st.text_input("Avance Cajas", value=current_data.get("Avance Cajas", "") if current_data else "")
        avance_empaque = st.text_input("Avance Empaque", value=current_data.get("Avance Empaque", "") if current_data else "")
        multiplicativo = st.text_input("Multiplicativo", value=current_data.get("Multiplicativo", "") if current_data else "")

    return (codigo, nombre, tipo_caja, primeras_segundas, cajas, avance, costo_cajas, precio_factura, avance_cajas, avance_empaque, multiplicativo)
def build_comision_form(current_data=None):
    """
    Create the form layout for editing or adding a Comision record.

    Args:
        current_data (dict, optional): Existing data to pre-fill the form (for editing).

    Returns:
        Tuple of str: Concepto (ID), Porcentaje fields.
    """
    col1, col2 = st.columns(2)
    with col1:
        concepto = st.text_input("Concepto", value=current_data.get("Concepto", "") if current_data else "")
    with col2:
        porcentaje = st.text_input("Porcentaje (%)", value=current_data.get("Porcentaje", "") if current_data else "")

    return concepto, porcentaje


# =========================================================
# Cajas Form Utility
# - Builds Streamlit form layouts for Cajas records
# =========================================================
def build_caja_form(current_data=None):
    """
    Create the form layout for editing or adding a Caja record.

    Args:
        current_data (dict, optional): Existing data to pre-fill the form (for editing).

    Returns:
        Tuple of str: Concepto, Multiplicativo, Caja, Panal, Liga, Flete Importa, Sueldos, 
                      Renta, Ryan, Empaque, Tags/Bags, Flete Locales fields.
        (Totales will be calculated separately.)
    """
    col1, col2, col3 = st.columns(3)
    with col1:
        concepto = st.text_input("Concepto", value=current_data.get("Concepto", "") if current_data else "")
        multiplicativo = st.text_input("Multiplicativo", value=current_data.get("Multiplicativo", "") if current_data else "")
        caja = st.text_input("Caja", value=current_data.get("Caja", "") if current_data else "")
        panal = st.text_input("Panal", value=current_data.get("Panal", "") if current_data else "")
    with col2:
        liga = st.text_input("Liga", value=current_data.get("Liga", "") if current_data else "")
        flete_importa = st.text_input("Flete Importa", value=current_data.get("Flete Importa", "") if current_data else "")
        sueldos = st.text_input("Sueldos", value=current_data.get("Sueldos", "") if current_data else "")
        renta = st.text_input("Renta", value=current_data.get("Renta", "") if current_data else "")
    with col3:
        ryan = st.text_input("Ryan", value=current_data.get("Ryan", "") if current_data else "")
        empaque = st.text_input("Empaque", value=current_data.get("Empaque", "") if current_data else "")
        tags_bags = st.text_input("Tags/Bags", value=current_data.get("Tags/Bags", "") if current_data else "")
        flete_locales = st.text_input("Flete Locales", value=current_data.get("Flete Locales", "") if current_data else "")

    return (
        concepto, multiplicativo, caja, panal, liga, flete_importa, sueldos, 
        renta, ryan, empaque, tags_bags, flete_locales
    )