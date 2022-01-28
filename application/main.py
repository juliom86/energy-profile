import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import time
import os
from application import column_builder, routes, country
# from application.functions import convert_df

def run():
    env = os.getenv('FLASK_ENV')

    if (env == 'dev'):
        BASE_URL = "http://localhost:8000"
    else:
        BASE_URL = "https://api-v4-s6r4cnmwdq-ew.a.run.app"

    routes.tabs()

    if st.sidebar.button('Solicitar información'):
        country.run()

    else:
        st.write(
            '''Un perfil energético completo de Argentina, sus provincias
            y regiones.
            Se puede acceder a información sobre el suministro y consumo de
            energía en GW.
            Centrales eléctricas de cada provincia.
            Generación por central y tipo de central.'''
        )
