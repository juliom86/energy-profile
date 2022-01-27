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
# from application.functions import convert_df

env = os.getenv('FLASK_ENV')

if (env == 'dev'):
    BASE_URL = "http://localhost:8000"
else:
    BASE_URL = "https://api-v4-s6r4cnmwdq-ew.a.run.app"


def run():
    api_request_progress_bar = st.progress(0)
    st.title("Producción vs. consumo de energía")
    col1, col2 = st.columns([3, 1])
    col3, col4 = st.columns([3, 1])
    col5, col6 = st.columns([3, 1])
    col7, col8 = st.columns([3, 1])
    col9, col10 = st.columns([3, 1])

    if st.sidebar.button('Solicitar información'):
        params = {
            "start_year": "2010",
            "end_year": "2020",
            "kpi": "all"
        }
        response = requests.get(BASE_URL + "/kpi", params=params)
        data = response.json()

        for percent_complete in range(100):
            time.sleep(0.01)
            api_request_progress_bar.progress(percent_complete + 1)

        api_request_progress_bar.empty()

        df_gen_vs_con = pd.read_json(data)

        col1.subheader("Generación Historica nivel pais en Argentina")

        generation_fig = px.line(
            df_gen_vs_con,
            x='Fecha',
            y='Generación GWh',
            width=1100,
            height=600)

        col1.plotly_chart(generation_fig)

        with col2:
            with st.expander("Mayor información y descarga de datos."):
                st.write("""
                    The chart above shows some numbers I picked for you.
                    I rolled actual dice for these, so they're *guaranteed* to
                    be random.
                """)

        col3.subheader("Consumo histórica nivel pais en Argentina")
        consumption_fig = px.line(
            df_gen_vs_con,
            x='Fecha',
            y='Consumo GWh',
            width=1100,
            height=600)

        col3.plotly_chart(consumption_fig)

        col3.subheader("Consumo per cápita historica Argentina")
        consumption_per_capita_fig = px.line(
            df_gen_vs_con,
            x='Fecha',
            y='Consumo per capita kWh',
            title='Consumo Percapita Historica Argentina')


        col5.plotly_chart(generation_fig)

        # Emisions
        params = {"start_year": "2010", "end_year": "2020", "fuels": "all"}
        response = requests.get(BASE_URL + "/emisions", params=params)
        data = response.json()

        df_emissions = pd.read_json(data)
        year = df_emissions['FECHA']
        liquid_fuel = df_emissions['de combustible líquido']
        gas_fuel    = df_emissions['de combustible gaseoso']
        solid_fuel  = df_emissions['de combustibles sólidos']

        col7.subheader(
            "Emisones de CO2 por consumo de combustible en la generación de energía"
        )
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(x=year, y=liquid_fuel, mode='lines', name='líquido'))
        fig.add_trace(
            go.Scatter(x=year, y=gas_fuel, mode='lines', name='gaseoso'))
        fig.add_trace(
            go.Scatter(x=year, y=solid_fuel, mode='lines', name='solido'))

        fig.update_layout(xaxis_title='Año',
                        yaxis_title='Emisiones por consumo de combustible')

        col7.plotly_chart(fig)


        #Mapa
        m = folium.Map(location=[-34.61315, -58.37723], zoom_start=4)
        provincia_argjson = gpd.read_file('./datasets/provincia.json')
        provincia_argjson = provincia_argjson[['nam', 'geometry']]
        df_cant = pd.read_excel(
            './datasets/cant_centr_prov_pobl_consumo_modificado.xlsx')
        df_final = provincia_argjson.merge(df_cant,
                                           left_on="nam",
                                           right_on="Provincia",
                                           how="outer")
        style_function = lambda x: {'fillColor': '#ffffff',
                            'color':'#000000',
                            'fillOpacity': 0.1,
                            'weight': 0.1}
        highlight_function = lambda x: {'fillColor': '#000000',
                                'color':'#000000',
                                'fillOpacity': 0.50,
                                'weight': 0.1}
        datos = folium.features.GeoJson(
                    data=df_final,

                    style_function=style_function,
                    control=False,
                    highlight_function=highlight_function,
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['Provincia',
                                'Nro_de_centrales',
                                'Población_2020',
                                'Consumo_total_por_población_provincia_GW','TERMICA', 'EOLICA', 'HIDRAULICA', 'NUCLEAR', 'RENOVABLES,'
                               ],
                        aliases=['Provincia',
                                'Nro de centrales',
                                'Población 2020',
                                 'Consumo total por población provincia GW','TERMICA', 'EOLICA', 'HIDRAULICA', 'NUCLEAR', 'RENOVABLES'
                                ],

                        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))



        m.add_child(datos)

        folium_static(m)

    else:
        st.write('Introducción al Proyecto')
