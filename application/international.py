import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import os


def run():
    env = os.getenv('FLASK_ENV')

    if (env == 'dev'):
        BASE_URL = "http://localhost:8000"
    else:
        BASE_URL = "https://api-v6-s6r4cnmwdq-ew.a.run.app"

    # International Profile
    col1, col2 = st.columns([4, 2])
    col3, col4 = st.columns([4, 2])

    # International Tab
    import_export = pd.read_csv(
        'datasets/Exportaciones e importaciones historicas.csv', sep=';')

    ## Exportation
    fig_export = px.bar(import_export,
                 x="Año",
                 color="pais",
                 y='Exportación',
                 title="Exportaciones de energía desde Argentina",
                 barmode='group',
                 height=600)

    ## Importation
    fig_import = px.bar(import_export,
                 x="Año",
                 color="pais",
                 y='Importación',
                 title="Importación de energía de Argentina",
                 barmode='group',
                 height=600)

    col1.plotly_chart(fig_export)

    with col2:
        st.write("""
            #### Exportaciones
            Si existen excedentes de energía eléctrica generada se exportan a países vecinos. .
        """)

    col3.plotly_chart(fig_import)

    with col4:
        st.write("""
            #### Importaciones
            Se importa energía eléctrica de otros países cuando los de los centros de producción de energía están muy alejados.
        """)
