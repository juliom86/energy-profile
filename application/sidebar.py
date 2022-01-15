import streamlit as st
import datetime

def run():
    st.sidebar.markdown(f"""
        # Energy Profile
        """)

    st.sidebar.markdown(f"""
        Puedes encontrar información sobre las variables disponibles [aquí](/glosary).
        """)

    st.sidebar.markdown(f"""
        ### Consulta de Datos:
        """)

    st.sidebar.multiselect('Seleccione el lugar de búsqueda', [
        'Argentina', 'Misiones', 'Chubut', 'Santa Cruz', 'Neuquen', 'Buenos Aires'
    ], ['Argentina'])

    st.sidebar.date_input("Seleccione la fecha de inicio",
                        datetime.date(2022, 1, 1))

    st.sidebar.date_input("Seleccione la fecha de fin", datetime.date(2022, 1, 1))
