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
        st.write('Introducción escrita por Mandy')
