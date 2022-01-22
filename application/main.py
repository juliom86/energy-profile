import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import time
# from application.functions import convert_df

BASE_URL = "https://api-v4-s6r4cnmwdq-ew.a.run.app"


def run():
    api_request_progress_bar = st.progress(0)
    st.title("Producción vs. consumo de energía")
    col1, col2 = st.columns([3, 1])
    col3, col4 = st.columns([3, 1])

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

    else:
        st.write('')
