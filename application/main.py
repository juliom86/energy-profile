import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
# from application.functions import convert_df

def run():
    api_request_progress_bar = st.progress(0)
    st.title("Producción vs. consumo de energía")
    col1, col2 = st.columns([3, 1])
    col3, col4 = st.columns([3, 1])

    if st.sidebar.button('Solicitar información'):
        for percent_complete in range(100):
            time.sleep(0.01)
            api_request_progress_bar.progress(percent_complete + 1)

        api_request_progress_bar.empty()

        df_gen_vs_con = pd.read_csv('datasets/gen_vs_con.csv')

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
