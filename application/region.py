import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import os


def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')

def run():

    env = os.getenv('FLASK_ENV')

    if (env == 'dev'):
        BASE_URL = "http://localhost:8000"
    else:
        BASE_URL = "https://api-v6-s6r4cnmwdq-ew.a.run.app"

    # Region Profile
    col1, col2 = st.columns([4, 2])
    col3, col4 = st.columns([4, 2])

    # Region Tab
    response = requests.get(BASE_URL + "/regions")
    data = response.json()

    demand_df = pd.read_json(data)
    demand_df= demand_df.fillna(0)

    ## Temperatura diaria por región

    fig_temp = px.line(demand_df,
                x='Fecha',
                y='Tem.Ayer',
                color='Región',
                width=1100,
                height=600,
                title="Temperatura diaria por región- 5 feb 2022")


    ## Consumo Diario por región

    fig_con = px.line(demand_df,
                x='Fecha',
                y='Dem.Ayer',
                color='Región',
                width=1100,
                height=600,
                title="Consumo diario por región- 5 feb 2022")

    col1.plotly_chart(fig_temp)

    with col2:
        st.write("""
            #### Temperatura diaria
            Corresponde a las mediciones de temperatura realizadas a diferentes horas del dìa en cada región del país.
        """)
        st.write("**Fuente:** [CAMMESA](https://portalweb.cammesa.com/default.aspx)")
        temperature_csv = convert_df(demand_df)
        st.download_button(label="Descargar dataset en CSV",
                           data=temperature_csv,
                           file_name='temperature.csv',
                           mime='text/csv',
                           key="1")
        st.write("""
                 ---
                 """)
        st.write("**API Endpoint**")
        st.write("""
                 Puedes realizar el request a `/regions` sin ningún paramtro.

                 👉 [Ver documentación completa](https://documenter.getpostman.com/view/5438737/UVXnGENw)
                 """)

    col3.plotly_chart(fig_con)

    with col4:
        st.write("""
            #### Consumo diario
            Corresponde a las mediciones de consumo realizadas a diferentes horas del día en cada región del país.
        """)
        st.write("**Fuente:** [CAMMESA](https://portalweb.cammesa.com/default.aspx)")
        consumption_csv = convert_df(demand_df)
        st.download_button(label="Descargar dataset en CSV",
                           data=consumption_csv,
                           file_name='consumption.csv',
                           mime='text/csv',
                           key="1")
        st.write("""
                 ---
                 """)
        st.write("**API Endpoint**")
        st.write("""
                 Puedes realizar el request a `/regions` sin ningún paramtro.

                 👉 [Ver documentación completa](https://documenter.getpostman.com/view/5438737/UVXnGENw)
                 """)
