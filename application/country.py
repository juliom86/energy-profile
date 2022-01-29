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
        BASE_URL = "https://api-v4-s6r4cnmwdq-ew.a.run.app"

    # Country Profile
    col1, col2 = st.columns([3, 1])
    col3, col4 = st.columns([3, 1])
    col5, col6 = st.columns([3, 1])
    col7, col8 = st.columns([3, 1])

    # Consumption and Generation API call
    params = {
        "start_year": "1980",
        "end_year": "2015",
        "kpi": "all"
    }
    response = requests.get(BASE_URL + "/kpi", params=params)
    data = response.json()

    df_gen_vs_con = pd.read_json(data)

    # Emissions API call

    params = {"start_year": "1980", "end_year": "2015", "fuel": "all"}
    response = requests.get(BASE_URL + "/emisions", params=params)
    data = response.json()

    df_emissions = pd.read_json(data)
    year = df_emissions['FECHA']
    liquid_fuel = df_emissions['de combustible líquido']
    gas_fuel    = df_emissions['de combustible gaseoso']
    solid_fuel  = df_emissions['de combustibles sólidos']

    # Country Tab
    ## Generation
    generation_fig = px.line(
        df_gen_vs_con,
        x='Fecha',
        y='Generación GWh',
        title='Generación Energética Historica Argentina',
        width=1100,
        height=600)
    consumption_fig = px.line(
        df_gen_vs_con,
        x='Fecha',
        y='Consumo GWh',
        title='Consumo Energético Historico Argentina',
        width=1100,
        height=600)

    col1.plotly_chart(generation_fig)

    with col2:
        st.write("""
            #### Fuente e información
            La generación de energía eléctrica engloba al conjunto de procesos distintos a través de los cuales puede producirse electricidad, o lo que es lo mismo, transformar otras formas de energía disponibles en la naturaleza (energía química, cinética, térmica, lumínica, nuclear, etc.) en energía eléctrica aprovechable.
        """)
        with st.expander("Mayor información y descarga de datos."):
            st.write("API and download button should go here.")

    col3.plotly_chart(consumption_fig)

    with col4:
        st.write("""
            #### Fuente e información
            El consumo energético es el gasto total de la energía, y normalmente incluye más de una fuente energética.
        """)
        with st.expander("Mayor información y descarga de datos."):
            st.write("API and download button should go here.")

    consumption_per_capita_fig = px.line(
        df_gen_vs_con,
        x='Fecha',
        y='Consumo per capita kWh',
        title='Consumo Percapita Historico Argentina',
        width=1100,
        height=600)

    col5.plotly_chart(consumption_per_capita_fig)

    with col6:
        st.write("""
            #### Fuente e información
            Consumo de enegía primaria por habitante.
            """)
        with st.expander("Mayor información y descarga de datos."):
            st.write("API and download button should go here.")


    # Emissions
    emissions_fig = go.Figure()
    emissions_fig.add_trace(
        go.Scatter(x=year, y=liquid_fuel, mode='lines', name='líquido'))
    emissions_fig.add_trace(
        go.Scatter(x=year, y=gas_fuel, mode='lines', name='gaseoso'))
    emissions_fig.add_trace(
        go.Scatter(x=year, y=solid_fuel, mode='lines', name='solido'))

    emissions_fig.update_layout(
        xaxis_title='Año',
        yaxis_title='Emisiones por consumo de combustible',
        width=1100,
        height=600,
        title='Emisiones por consumo de combustible',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.89
        )
    )

    col7.plotly_chart(emissions_fig)

    with col8:
        st.write("""
            #### Fuente e información
            Hace referencia a las emisiones generadas como resultado de la generación energética, usando combustibles líquidos, sólidos o gaseosos.
        """)
        with st.expander("Mayor información y descarga de datos."):
            st.write("API and download button should go here.")
