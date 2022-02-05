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

    # Region Profile
    col1, col2 = st.columns([4, 2])
    col3, col4 = st.columns([4, 2])

    # Region Tab
    demanda_temp= pd.read_csv('datasets/Regiones_DemandaYTemperatura_05022022.csv',sep = ';')
    demanda_temp= demanda_temp.fillna(0)

    ## Temperatura diaria por región

    fig_temp = px.line(demanda_temp,
                x='Fecha',
                y='Tem.Ayer',
                color='Región',
                width=1100,
                height=600,
                title="Temperatura diaria por región- 5 feb 2022")


    ## Consumo Diario por región

    fig_con = px.line(demanda_temp,
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

    col3.plotly_chart(fig_con)

    with col4:
        st.write("""
            #### Consumo diario
            Corresponde a las mediciones de consumo realizadas a diferentes horas del día en cada región del país.
        """)
