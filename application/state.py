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



    # 1 Crear dataframe desde el dataset
    df_fact = pd.read_csv('./datasets/fact_prov.csv')
    df_pot_inst = pd.read_csv('./datasets/pot_inst.csv')

    # Selecciono provincia del dataset y filtro
    bs_as=df_fact[df_fact['Provincia'] == 'Buenos Aires']

    categoria = ['Residencial', 'Comercial', 'Industrial', 'Saniratios', 'Alumbrado', 'Oficial', 'Rural', 'Otros', 'Traccion']

    valores = [bs_as.Residencial.sum(), bs_as.Comercial.sum(), bs_as.Industrial.sum(), bs_as['S. Sanitarios'].sum(),
          bs_as.Riego.sum(), bs_as.Oficial.sum(), bs_as['E. Rural'].sum(), bs_as.Otros.sum(), bs_as['Tracción'].sum()]

    tipos_df = pd.DataFrame({'zonas': categoria, 'Mwh Facturado': valores})

    pot_bsas = df_pot_inst[df_pot_inst['Provincia']=='Buenos Aires']

    plantas = ['Ciclo_conbinado', 'Motor_Diesel', 'Turbina_Gas', 'Turbina_Vapor',
           'Hidraulica', 'Nuclear', 'GeoTerm', 'Eolica', 'Solar']

    energia = [pot_bsas.Ciclo_conbinado.sum(), pot_bsas.Motor_Diesel.sum(), pot_bsas.Turbina_Gas.sum(),
          pot_bsas.Turbina_Vapor.sum(), pot_bsas.Hidraulica.sum(), pot_bsas.Nuclear.sum(), pot_bsas.GeoTerm.sum(),
           pot_bsas.Eolica.sum(), pot_bsas.Solar.sum()
          ]

    tipos_pot_df = pd.DataFrame({'plantas':plantas,
                        'energia':energia})


    # 3 Crear la figura a partit del data frame
    fig1 = px.line(bs_as,
                             x='Año',
                             y='Total',
                             title='Total energia facturada en MWh',
                             width=1100,
                             height=600)
    fig1.update_layout(xaxis=dict(rangeselector=dict(buttons=list([
        dict(count=1, label="1y", step="year", stepmode="backward"),
        dict(step="all")
    ])), rangeslider=dict(visible=True)))

    fig2 = px.line(pot_bsas,
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

    #fig.add_trace(go.Bar(x=tipos_df['Mwh Facturado'], y=tipos_df['zonas'], orientation='h'),
    #        row=2, col=1)

    #fig.add_trace(go.Bar(x=tipos_pot_df['plantas'], y=tipos_pot_df['energia']),
    #         row=2, col=2)




    ## Generation

    col1.plotly_chart(fig1)

    with col2:
        st.write("""
            #### Generación
            La generación de energía eléctrica engloba al conjunto de procesos distintos a través de los cuales puede producirse electricidad, o lo que es lo mismo, transformar otras formas de energía disponibles en la naturaleza (energía química, cinética, térmica, lumínica, nuclear, etc.) en energía eléctrica aprovechable.
        """)
        st.write("**Fuente:** [XXXXXXXXX](https://www.lewagon.com)")
        facturacion_csv = convert_df(bs_as[['Año', 'Total']])
        st.download_button(label="Descargar dataset en CSV",
                           data=facturacion_csv,
                           file_name='facturacion_historica.csv',
                           mime='text/csv',
                           key="1")
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



    col3.plotly_chart(fig2)

    with col4:
        st.write("""
            #### Generación
            La generación de energía eléctrica engloba al conjunto de procesos distintos a través de los cuales puede producirse electricidad, o lo que es lo mismo, transformar otras formas de energía disponibles en la naturaleza (energía química, cinética, térmica, lumínica, nuclear, etc.) en energía eléctrica aprovechable.
        """)
        st.write("**Fuente:** [XXXXXXXXX](https://www.lewagon.com)")
        potencia_csv = convert_df(pot_bsas[['Año', 'Potencia Total']])
        st.download_button(label="Descargar dataset en CSV",
                           data=potencia_csv,
                           file_name='Potencia_historica.csv',
                           mime='text/csv',
                           key="1")
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
                           file_name='zonas.csv',
                           mime='text/csv',
                           key="1")
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
                           file_name='tipos.csv',
                           mime='text/csv',
                           key="1")
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
