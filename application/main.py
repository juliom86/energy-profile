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
        BASE_URL = "http://localhost:8000"
    else:
        BASE_URL = "https://api-v5-s6r4cnmwdq-ew.a.run.app"

    routes.tabs()

    query_params = st.experimental_get_query_params()

    if "tab" in query_params:
        active_tab = query_params["tab"][0]
        if active_tab == 'País':
            st.write("""
                     ## Perfil energético de Argentina
                     Seleccione las opciones sobre la navegación para solicitar información sobre el perfil energético de Argentina.
                    - Lugar de búsqueda
                    - Años de búsqueda
                    - ...

                     ---
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
