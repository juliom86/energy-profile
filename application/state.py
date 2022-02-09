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

    # Filter BA if `selected_region` is Argentina
    if selected_region == 'Argentina':
        st.write("Primero debe solicitar una provincia.")
    else:
        # Country Profile
        col1, col2 = st.columns([4, 2])
        col3, col4 = st.columns([4, 2])
        col5, col6 = st.columns([4, 2])
        col7, col8 = st.columns([4, 2])


        # 1 Crear dataframe desde el dataset
        params = {"start_year": "1970", "end_year": "2012", "state": selected_region}

        response = requests.get(BASE_URL + "/billing", params=params)
        data = response.json()

        state_df = pd.read_json(data)

        params = {"start_year": "1976", "end_year": "2012", "state": selected_region}
        response = requests.get(BASE_URL + "/power", params=params)
        data = response.json()

        state_pot_df = pd.read_json(data)

        categoria = ['Residencial', 'Comercial', 'Industrial', 'Saniratios', 'Alumbrado', 'Oficial', 'Rural', 'Otros', 'Traccion']

        valores = [state_df.Residencial.sum(), state_df.Comercial.sum(), state_df.Industrial.sum(), state_df['S. Sanitarios'].sum(),
            state_df.Riego.sum(), state_df.Oficial.sum(), state_df['E. Rural'].sum(), state_df.Otros.sum(), state_df['Tracción'].sum()]

        tipos_df = pd.DataFrame({'zonas': categoria, 'Mwh Facturado': valores})



        plantas = ['Ciclo_conbinado', 'Motor_Diesel', 'Turbina_Gas', 'Turbina_Vapor',
            'Hidraulica', 'Nuclear', 'GeoTerm', 'Eolica', 'Solar']

        energia = [state_pot_df.Ciclo_conbinado.sum(), state_pot_df.Motor_Diesel.sum(), state_pot_df.Turbina_Gas.sum(),
            state_pot_df.Turbina_Vapor.sum(), state_pot_df.Hidraulica.sum(), state_pot_df.Nuclear.sum(), state_pot_df.GeoTerm.sum(),
            state_pot_df.Eolica.sum(), state_pot_df.Solar.sum()
            ]

        tipos_pot_df = pd.DataFrame({'plantas':plantas,
                            'energia':energia})


        # 3 Crear la figura a partit del data frame
        fig1 = px.line(state_df,
                        x='Año',
                        y='Total',
                        title='Total energia facturada en MWh',
                        width=1100,
                        height=600)
        fig1.update_layout(xaxis=dict(rangeselector=dict(buttons=list([
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])), rangeslider=dict(visible=True)))

        fig2 = px.line(state_pot_df,
                    x='Año',
                    y='Potencia Total',
                    title='Potencia instalada',
                    width=1100,
                    height=600)
        fig2.update_layout(xaxis=dict(rangeselector=dict(buttons=list([
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])),
                                    rangeslider=dict(visible=True)))


        fig3 = px.bar(tipos_df,
                    x="Mwh Facturado",
                    y="zonas",
                    orientation='h',
                    width=1100,
                    height=600)
        fig4 = px.bar(tipos_pot_df,
                    x="plantas",
                    y="energia",
                    width=1100,
                    height=600)



        col1.plotly_chart(fig1)

        with col2:
            st.write("""
                #### Generación
                La generación de energía eléctrica engloba al conjunto de procesos distintos a través de los cuales puede producirse electricidad, o lo que es lo mismo, transformar otras formas de energía disponibles en la naturaleza (energía química, cinética, térmica, lumínica, nuclear, etc.) en energía eléctrica aprovechable.
            """)
            st.write("**Fuente:** [XXXXXXXXX](https://www.lewagon.com)")
            facturacion_csv = convert_df(state_df[['Año', 'Total']])
            st.download_button(
                label="Descargar dataset en CSV",
                data=facturacion_csv,
                file_name=f"facturacion_historica_{selected_region}.csv",
                mime='text/csv',
                key="1")
            st.write("""
                    ---
                    """)
            st.write("**API Endpoint**")
            st.write("""
                    Puedes realizar el request a `/billing` con los siguientes paramtros obligatorios:
                    - `start_year`: entero y desde 1970 la fecha
                    - `end_year`: entero y desde 1970 a la fecha
                    - `state`: Capital Federal, Buenos Aires, Catamarca, Córdoba, Corrientes, Chaco, Chubut, Entre Ríos, Formosa, Jujuy, La Pampa, La Rioja, Mendoza, Misiones, Neuquén, Rio Negro, Salta, San Juan, San Luis, Santa Cruz, Santa Fé, Santiago del Estero, Tierra del Fuego

                    👉 [Ver documentación completa](https://documenter.getpostman.com/view/5438737/UVXnGENw)
                    """)



        col3.plotly_chart(fig2)

        with col4:
            st.write("""
                #### Generación
                La generación de energía eléctrica engloba al conjunto de procesos distintos a través de los cuales puede producirse electricidad, o lo que es lo mismo, transformar otras formas de energía disponibles en la naturaleza (energía química, cinética, térmica, lumínica, nuclear, etc.) en energía eléctrica aprovechable.
            """)
            st.write("**Fuente:** [XXXXXXXXX](https://www.lewagon.com)")
            potencia_csv = convert_df(state_pot_df[['Año', 'Potencia Total']])
            st.download_button(
                label="Descargar dataset en CSV",
                data=potencia_csv,
                file_name=f"potencia_historica_{selected_region}.csv",
                mime='text/csv',
                key="1")
            st.write("""
                    ---
                    """)
            st.write("**API Endpoint**")
            st.write("""
                    Puedes realizar el request a `/power` con los siguientes paramtros obligatorios:
                    - `start_year`: entero y desde 1976 la fecha
                    - `end_year`: entero y desde 1976 a la fecha
                    - `state`: Capital Federal, Buenos Aires, Catamarca, Córdoba, Corrientes, Chaco, Chubut, Entre Ríos, Formosa, Jujuy, La Pampa, La Rioja, Mendoza, Misiones, Neuquén, Rio Negro, Salta, San Juan, San Luis, Santa Cruz, Santa Fé, Santiago del Estero, Tierra del Fuego

                    👉 [Ver documentación completa](https://documenter.getpostman.com/view/5438737/UVXnGENw)
                    """)


        col5.plotly_chart(fig3)

        with col6:
            st.write("""
                #### Generación
                La generación de energía eléctrica engloba al conjunto de procesos distintos a través de los cuales puede producirse electricidad, o lo que es lo mismo, transformar otras formas de energía disponibles en la naturaleza (energía química, cinética, térmica, lumínica, nuclear, etc.) en energía eléctrica aprovechable.
            """)
            st.write("**Fuente:** [XXXXXXXXX](https://www.lewagon.com)")
            zonas_csv = convert_df(tipos_df[['zonas', 'Mwh Facturado']])
            st.download_button(label="Descargar dataset en CSV",
                            data=zonas_csv,
                            file_name=f"zonas_{selected_region}.csv",
                            mime='text/csv',
                            key="1")
            st.write("""
                    ---
                    """)
            st.write("**API Endpoint**")
            st.write("""
                        No existe endpoint para esta información.
                    """)



        col7.plotly_chart(fig4)

        with col8:
            st.write("""
                #### Generación
                La generación de energía eléctrica engloba al conjunto de procesos distintos a través de los cuales puede producirse electricidad, o lo que es lo mismo, transformar otras formas de energía disponibles en la naturaleza (energía química, cinética, térmica, lumínica, nuclear, etc.) en energía eléctrica aprovechable.
            """)
            st.write("**Fuente:** [XXXXXXXXX](https://www.lewagon.com)")
            tipos_csv = convert_df(tipos_pot_df[["plantas", "energia"]])
            st.download_button(label="Descargar dataset en CSV",
                            data=tipos_csv,
                            file_name=f"tipos_{selected_region}.csv",
                            mime='text/csv',
                            key="1")
            st.write("""
                    ---
                    """)
            st.write("**API Endpoint**")
            st.write("""
                        No existe endpoint para esta información.
                    """)
