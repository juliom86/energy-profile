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
from application import routes, country, map, international, region
# from application.functions import convert_df

def run(selected_option = 'Argentina'):
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
            st.write(
            """
            ## Perfil País
              - Encuentra cifras historicas del comportamiento enérgetico de Argentina.
              - Selecciona el periodo de tiempo que quieres analizar.
              - Descarga las gráficas.
              - Accede a la fuente.
              - Descarga el dataset.
              - Consume la información a través de la API.
            """
            )

            st.write("""
                        ## Resultado de la búsqueda
                        ---
                """)
            # Country
            country.run(selected_option)
        if active_tab == 'Mapa':
            st.write(
            '''
            ## Mapa
              - Encuentra cifras historicas del comportamiento enérgetico de cada provincia en Argentina.
              - Pasando el cursor por encima de una provincia accede a información sobre problación y consumo energético.
              - Con un click en el point accede a gráficas:
                  - Consumo energético histórico por provincia.
                  - Potencia instalada histórico por provincia.
                  - Usos de la energía por provincia.
                  - Tipos de plantas energéticas.
              - Descarga la grafica presionando ... en la parte superior derecha del mismo.
            '''
            )
            # Map
            map.run()
         # International
        if active_tab == 'Internacional':
            st.write(
            '''
            ## Intercambios de Energía
              - Accede a cifras históricas de importaciones y exportaciones.
              - Selecciona en el gráfico el pais del que quieres tener el análisis.
              - Descarga las gráficas.
              - Accede a la fuente.
              - Descarga el dataset.
              - Consume la información a través de la API.
            '''
            )
            international.run()
        # Region
        if active_tab == 'Región':
            st.write(
            '''
            ## Regiones
              - Análisis de la relación de temperatura vs el consumo de energía por regiones en Argentina durante un día.
              - Selecciona en el gráfico la región del que quieres tener el análisis de temperatura y consumo en diferentes horas del día.
              - Descarga las gráficas.
              - Accede a la fuente.
              - Descarga el dataset.
              - Consume la información a través de la API.
            '''
            )
            region.run()

        if active_tab == 'API':
            pass
    else:

        st.image(
        "https://s1.1zoom.me/big0/568/Argentina_Houses_Roads_478950.jpg",
        width=1600
        )

        st.write(
        '''
        ## Perfil energético de Argentina
        La generación y el consumo de energía es una de las mayores fuentes de generación CO2 en el mundo.
        Solo se es consciente de la huella generada cuando se tiene la capacidad de medir el impacto.
        Inspirados en https://app.electricitymap.org/ iniciamos a construir el perfil enérgetico de Latino América, empezando por Argentina.
        Energy profile es un proyecto en construcción, que representa un primer acercamientoal perfil energético de Argentina.
        Encontrarás inicialmente información, gráficas y análitica sobre:
        - Consumo de energía
        - Generación de energía
        - Consumo per capita de energía
        - Emisiones por generación de energía
        - Otros...
        La información esta clasificada en 4 niveles:
        - Nivel País
        - Nivel Región
        - Nivel Provincia
        - Nivel Internacional
        Queremos contribuir en la generación de conocimiento sobre la energía y su impacto en el Medio Ambiente
        '''
        )
