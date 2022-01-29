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

    st.sidebar.multiselect('Seleccione el lugar de búsqueda', ['Argentina'])
