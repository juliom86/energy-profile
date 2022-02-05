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

    # International Profile
    col1, col2 = st.columns([4, 2])
    col3, col4 = st.columns([4, 2])

    # International Tab
    import_export_df = pd.read_csv(
        'datasets/Exportaciones e importaciones historicas.csv', sep=';')

    ## Exportation
    fig_export = px.bar(import_export_df,
                 x="Año",
                 color="pais",
                 y='Exportación',
                 title="Exportaciones de energía desde Argentina",
                 barmode='group',
                 height=600,
                 width=1100)

    ## Importation
    fig_import = px.bar(import_export_df,
                        x="Año",
                        color="pais",
                        y='Importación',
                        title="Importación de energía de Argentina",
                        barmode='group',
                        height=600,
                        width=1100)

    col1.plotly_chart(fig_export)

    with col2:
        st.write("""
            #### Exportaciones
            Si existen excedentes de energía eléctrica generada se exportan a países vecinos. .
        """)
        st.write("**Fuente:** [XXXXXXXXX](https://www.lewagon.com)")
        export_csv = convert_df(import_export_df[['Año', 'pais', 'Exportación']])
        st.download_button(label="Descargar dataset en CSV",
                           data=export_csv,
                           file_name='exportación_por_pais.csv',
                           mime='text/csv',
                           key="1")
        st.write("""
                 ---
                 """)
        st.write("**API Endpoint**")
        st.write("""
                 Puedes realizar el request a `/balance` con los siguientes paramtros obligatorios:
                 - `start_year`: entero y desde 2005 a 2019
                 - `end_year`: entero y desde 2005 a 2019
                 - `kpi`: `export`

                 👉 [Ver documentación completa](https://documenter.getpostman.com/view/5438737/UVXnGENw)
                 """)

    col3.plotly_chart(fig_import)

    with col4:
        st.write("""
            #### Importaciones
            Se importa energía eléctrica de otros países cuando los de los centros de producción de energía están muy alejados.
        """)
        st.write("**Fuente:** [XXXXXXXXX](https://www.lewagon.com)")
        exportacion_csv = convert_df(
            import_export_df[['Año', 'pais', 'Importación']])
        st.download_button(label="Descargar dataset en CSV",
                           data=exportacion_csv,
                           file_name='importacion_por_pais.csv',
                           mime='text/csv',
                           key="1")
        st.write("""
                 ---
                 """)
        st.write("**API Endpoint**")
        st.write("""
                 Puedes realizar el request a `/balance` con los siguientes paramtros obligatorios:
                 - `start_year`: entero y desde 2005 a 2019
                 - `end_year`: entero y desde 2005 a 2019
                 - `kpi`: `import`

                 👉 [Ver documentación completa](https://documenter.getpostman.com/view/5438737/UVXnGENw)
                 """)
