import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import time
import os
from application import column_builder, routes
# from application.functions import convert_df

def run():
    env = os.getenv('FLASK_ENV')

    if (env == 'dev'):
        BASE_URL = "http://localhost:8000"
    else:
        BASE_URL = "https://api-v4-s6r4cnmwdq-ew.a.run.app"

    routes.tabs()

    if st.sidebar.button('Solicitar información'):

        # Country Profile
        col1, col2 = st.columns([3, 1])
        col3, col4 = st.columns([3, 1])
        col5, col6 = st.columns([3, 1])
        col7, col8 = st.columns([3, 1])

        # Consumption and Generation API call
        params = {
            "start_year": "2010",
            "end_year": "2020",
            "kpi": "all"
        }
        response = requests.get(BASE_URL + "/kpi", params=params)
        data = response.json()

        df_gen_vs_con = pd.read_json(data)

        # Emissions API call

        params = {"start_year": "2010", "end_year": "2020", "fuels": "all"}
        response = requests.get(BASE_URL + "/emisions", params=params)
        data = response.json()

        df_emissions = pd.read_json(data)
        year = df_emissions['FECHA']
        liquid_fuel = df_emissions['de combustible líquido']
        gas_fuel    = df_emissions['de combustible gaseoso']
        solid_fuel  = df_emissions['de combustibles sólidos']

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(x=year, y=liquid_fuel, mode='lines', name='líquido'))
        fig.add_trace(
            go.Scatter(x=year, y=gas_fuel, mode='lines', name='gaseoso'))
        fig.add_trace(
            go.Scatter(x=year, y=solid_fuel, mode='lines', name='solido'))

        fig.update_layout(xaxis_title='Año',
                        yaxis_title='Emisiones por consumo de combustible')

        # Country Tab
        ## Generation
        generation_fig = px.line(
            df_gen_vs_con,
            x='Fecha',
            y='Generación GWh',
            width=1100,
            height=600)
        consumption_fig = px.line(
            df_gen_vs_con,
            x='Fecha',
            y='Consumo GWh',
            width=1100,
            height=600)

        column_builder.run(col1, generation_fig,
                   {
                       'title': 'Producción vs. consumo de energía',
                       'subheader': 'Generación Historica nivel pais en Argentina',
                       'description': 'Gráfico de la producción vs. consumo de energía en el país de Argentina.'
                    })

        with col2:
            with st.expander("Mayor información y descarga de datos."):
                st.write("""
                    The chart above shows some numbers I picked for you.
                    I rolled actual dice for these, so they're *guaranteed* to
                    be random.
                """)

        column_builder.run(col3, consumption_fig,
                   {
                       'title': 'Consumo histórica nivel pais en Argentina',
                       'subheader': '....',
                       'description': '...'
                    })

        with col4:
            with st.expander("Mayor información y descarga de datos."):
                st.write("""
                    The chart above shows some numbers I picked for you.
                    I rolled actual dice for these, so they're *guaranteed* to
                    be random.
                """)

        consumption_per_capita_fig = px.line(
            df_gen_vs_con,
            x='Fecha',
            y='Consumo per capita kWh',
            title='Consumo Percapita Historica Argentina')

        column_builder.run(col5, consumption_per_capita_fig,
                    {
                       'title': 'Consumo per cápita historica Argentina',
                       'subheader': '....',
                       'description': '...'
                    })

        with col6:
            with st.expander("Mayor información y descarga de datos."):
                st.write("""
                    The chart above shows some numbers I picked for you.
                    I rolled actual dice for these, so they're *guaranteed* to
                    be random.
                """)

        # Emissions
        column_builder.run(col7, df_emissions,
            {
                'title': 'Emisiones',
                'subheader': '....',
                'description': '...'
            })

        with col8:
            with st.expander("Mayor información y descarga de datos."):
                st.write("""
                    The chart above shows some numbers I picked for you.
                    I rolled actual dice for these, so they're *guaranteed* to
                    be random.
                """)

    else:
        st.write('Introducción al Proyecto')
