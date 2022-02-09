import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import os

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')


def run(selected_region):
    env = os.getenv('FLASK_ENV')

    if (env == 'dev'):
        BASE_URL = "http://localhost:8000"
    else:
        BASE_URL = "https://api-v6-s6r4cnmwdq-ew.a.run.app"

    # Filter if `selected_region`


    # Country Profile
    col1, col2 = st.columns([4, 2])
    col3, col4 = st.columns([4, 2])
    col5, col6 = st.columns([4, 2])
    col7, col8 = st.columns([4, 2])

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
    response = requests.get(BASE_URL + "/emissions", params=params)
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
        title='Generación Energética Histórica Argentina',
        width=1100,
        height=600)
    generation_fig.update_layout(xaxis=dict(rangeselector=dict(buttons=list([
        dict(count=1, label="1y", step="year", stepmode="backward"),
        dict(step="all")])),rangeslider=dict(visible=True)))

    consumption_fig = px.line(
        df_gen_vs_con,
        x='Fecha',
        y='Consumo GWh',
        title='Consumo Energético Histórico Argentina',
        width=1100,
        height=600)
    consumption_fig.update_layout(xaxis=dict(rangeselector=dict(buttons=list([
        dict(count=1, label="1y", step="year", stepmode="backward"),
        dict(step="all")])),rangeslider=dict(visible=True)))

    col1.plotly_chart(generation_fig)

    with col2:
        st.write("""
            #### Generación
            La generación de energía eléctrica engloba al conjunto de procesos distintos a través de los cuales puede producirse electricidad, o lo que es lo mismo, transformar otras formas de energía disponibles en la naturaleza (energía química, cinética, térmica, lumínica, nuclear, etc.) en energía eléctrica aprovechable.
        """)
        st.write("**Fuente:** [XXXXXXXXX](https://www.lewagon.com)")
        generation_csv = convert_df(df_gen_vs_con[['Fecha', 'Generación GWh']])
        st.download_button(
            label="Descargar dataset en CSV",
            data=generation_csv,
            file_name='generacion_historica_argentina.csv',
            mime='text/csv',
            key="1"
        )
        st.write("""
                 ---
                 """)
        st.write("**API Endpoint**")
        st.write("""
                 Puedes realizar el request a `/kpi` con los siguientes paramtros obligatorios:
                 - `start_year`: entero y desde 1980 la fecha
                 - `end_year`: entero y desde 1980 a la fecha
                 - `kpi`: `generation`

                 👉 [Ver documentación completa](https://documenter.getpostman.com/view/5438737/UVXnGENw)
                 """)

    col3.plotly_chart(consumption_fig)

    with col4:
        st.write("""
            #### Consumo
            El consumo energético es el gasto total de la energía, y normalmente incluye más de una fuente energética.
        """)
        st.write("**Fuente:** [XXXXXXXXX](https://www.lewagon.com)")
        consumption_csv = convert_df(df_gen_vs_con[['Fecha', 'Consumo GWh']])
        st.download_button(
            label="Descargar dataset en CSV",
            data=consumption_csv,
            file_name='consumo_energetico_historico_argentina.csv',
            mime='text/csv',
            key="2"
        )
        st.write("""
                 ---
                 """)
        st.write("**API Endpoint**")
        st.write("""
                 Puedes realizar el request a `/kpi` con los siguientes paramtros obligatorios:
                 - `start_year`: entero y desde 1980 la fecha
                 - `end_year`: entero y desde 1980 a la fecha
                 -  `kpi`: `consumption`

                 👉 [Ver documentación completa](https://documenter.getpostman.com/view/5438737/UVXnGENw)
                 """)

    consumption_per_capita_fig = px.line(
        df_gen_vs_con,
        x='Fecha',
        y='Consumo per capita kWh',
        title='Consumo Percapita Histórico Argentina',
        width=1100,
        height=600)
    consumption_per_capita_fig.update_layout(
        xaxis=dict(rangeselector=dict(buttons=list([
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")])),rangeslider=dict(visible=True)))

    col5.plotly_chart(consumption_per_capita_fig)

    with col6:
        st.write("""
            #### Consumo per cápita
            Consumo de enegía primaria por habitante.
        """)
        st.write("**Fuente:** [XXXXXXXXX](https://www.lewagon.com)")
        consumption_per_capita_csv = convert_df(
            df_gen_vs_con[['Fecha', 'Consumo per capita kWh']])
        st.download_button(
            label="Descargar dataset en CSV",
            data=consumption_per_capita_csv,
            file_name='consumo_energetico_per_capita_historico_argentina.csv',
            mime='text/csv',
            key="3"
        )
        st.write("""
                 ---
                 """)
        st.write("**API Endpoint**")
        st.write("""
                 Puedes realizar el request a `/kpi` con los siguientes paramtros obligatorios:
                 - `start_year`: entero y desde 1980 la fecha
                 - `end_year`: entero y desde 1980 a la fecha
                 - `kpi`: `consumption per capita`

                 👉 [Ver documentación completa](https://documenter.getpostman.com/view/5438737/UVXnGENw)
                 """)

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
        s
        title='Emisiones por consumo de combustible',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.89
        )
    )
    emissions_fig.update_layout(xaxis=dict(rangeselector=dict(buttons=list([
        dict(count=1, label="1y", step="year", stepmode="backward"),
        dict(step="all")])),rangeslider=dict(visible=True)))

    col7.plotly_chart(emissions_fig)

    with col8:
        st.write("""
            #### Emisiones
            Hace referencia a las emisiones generadas como resultado de la generación energética, usando combustibles líquidos, sólidos o gaseosos.
        """)
        st.write("**Fuente:** [XXXXXXXXX](https://www.lewagon.com)")
        df_emissions_csv = convert_df(df_emissions)
        st.download_button(
            label="Descargar dataset en CSV",
            data=df_emissions_csv,
            file_name='emisiones_segun_combustible.csv',
            mime='text/csv',
            key="4"
        )
        st.write("""
                 ---
                 """)
        st.write("**API Endpoint**")
        st.write("""
                 Puedes realizar el request a `/emissions` con los siguientes paramtros obligatorios:
                 - `start_year`: entero y desde 1980 la fecha
                 - `end_year`: entero y desde 1980 a la fecha
                 - `fuel`: texto con opciones `all`, `gas`, `liquid`, `solid`

                 👉 [Ver documentación completa](https://documenter.getpostman.com/view/5438737/UVXnGENw)
                 """)
