import streamlit as st
import datetime

def run():
    st.sidebar.markdown(f"""
        # Energy Profile
        """)


    st.sidebar.image(
        "https://fondosmil.com/fondo/12790.png",
        width=200
    )

    st.sidebar.markdown(f"""
        Puedes encontrar información sobre las variables disponibles [aquí](/glosary).
        """)

    st.sidebar.markdown(f"""
        ### Consulta de Datos:
        """)

    selected_region = st.sidebar.selectbox(
        'Seleccione el lugar de búsqueda',
        ('Argentina', 'Capital Federal', 'Buenos Aires', 'Catamarca',
         'Córdoba', 'Corrientes', 'Chaco', 'Chubut', 'Entre Ríos', 'Formosa',
         'Jujuy', 'La Pampa', 'La Rioja', 'Mendoza', 'Misiones', 'Neuquén',
         'Rio Negro', 'Salta', 'San Juan', 'San Luis', 'Santa Cruz',
         'Santa Fé', 'Santiago del Estero', 'Tierra del Fuego'))

    return selected_region
