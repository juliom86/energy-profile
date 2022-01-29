import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import time
import os
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from application import routes, country, map
# from application.functions import convert_df

def run():
    env = os.getenv('FLASK_ENV')

    if (env == 'dev'):
        BASE_URL = "http://localhost:8001"
    else:
        BASE_URL = "https://api-v6-s6r4cnmwdq-ew.a.run.app"

    routes.tabs()

    query_params = st.experimental_get_query_params()

    if "tab" in query_params:
        active_tab = query_params["tab"][0]
        if active_tab == 'País':
            st.write("""
                     ## Perfil energético de Argentina
                     La generación y el consumo de energía es una de las mayores fuentes de generación CO2 en el mundo.
                     Solo se es consciente de la huella generada cuando se tiene la capacidad de medir el impacto.
                     Energy profile es un proyecto en construcción, que representa un primer acercamiento
                     al perfil energético de Argentina. Encontrarás inicialmente:
                    - Consumo
                    - Generación
                    - Consumo per capita
                    - Emisiones por generación de energía
                    - Otros...

                    Queremos contribuir en la generación de conocimiento sobre la energía y su impacto en el MA
                     """)
            if st.sidebar.button('Solicitar información'):
                st.write("""
                         ## Resultado de la búsqueda
                    """)
                # Country
                country.run()
        if active_tab == 'Mapa':
            # Map
            map.run()
    else:
        st.write(
            '''Un perfil energético completo de Argentina, sus provincias
            y regiones.
            Se puede acceder a información sobre el suministro y consumo de
            energía en GW.
            Centrales eléctricas de cada provincia.
            Generación por central y tipo de central.'''
        )
