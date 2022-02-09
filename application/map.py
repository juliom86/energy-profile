import pandas as pd
import geopandas as gpd
import folium
import requests
import altair as alt
import os
from streamlit_folium import folium_static

df_fact = pd.read_csv('./datasets/fact_prov.csv')
df_pot_inst = pd.read_csv('./datasets/pot_inst.csv')
df_coord = pd.read_csv('./datasets/provincias.csv')


def generar_marker(state):

    df_f = df_fact[df_fact['Provincia'] == state]

    categoria = [
        'Residencial', 'Comercial', 'Industrial', 'Saniratios', 'Alumbrado',
        'Oficial', 'Rural', 'Otros', 'Traccion'
    ]

    valores = [
        df_f.Residencial.sum(),
        df_f.Comercial.sum(),
        df_f.Industrial.sum(), df_f['S. Sanitarios'].sum(),
        df_f.Riego.sum(),
        df_f.Oficial.sum(), df_f['E. Rural'].sum(),
        df_f.Otros.sum(), df_f['Tracción'].sum()
    ]

    tipos_df = pd.DataFrame({'zonas': categoria, 'Mwh Facturado': valores})

    df_pot = df_pot_inst[df_pot_inst['Provincia'] == state]

    plantas = [
        'Ciclo_conbinado', 'Motor_Diesel', 'Turbina_Gas', 'Turbina_Vapor',
        'Hidraulica', 'Nuclear', 'GeoTerm', 'Eolica', 'Solar'
    ]

    energia = [
        df_pot.Ciclo_conbinado.sum(),
        df_pot.Motor_Diesel.sum(),
        df_pot.Turbina_Gas.sum(),
        df_pot.Turbina_Vapor.sum(),
        df_pot.Hidraulica.sum(),
        df_pot.Nuclear.sum(),
        df_pot.GeoTerm.sum(),
        df_pot.Eolica.sum(),
        df_pot.Solar.sum()
    ]

    tipos_pot_df = pd.DataFrame({'plantas': plantas, 'energia': energia})

    fig1 = alt.Chart(df_f).mark_line().encode(x='Año',
                                              y='Total').properties(width=150,
                                                                    height=150)
    fig2 = alt.Chart(tipos_df).mark_bar().encode(
        x='Mwh Facturado', y='zonas').properties(width=150, height=150)
    fig3 = alt.Chart(df_pot).mark_line().encode(
        x='Año', y='Potencia Total').properties(width=150, height=150)
    fig4 = alt.Chart(tipos_pot_df).mark_bar().encode(
        x='plantas', y='energia').properties(width=150, height=150)

    prov = df_coord[df_coord['iso_nombre'] == state]
    lat = prov['latitud']
    lon = prov['longitud']

    marker = folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(max_width=500).add_child(
            folium.VegaLite(fig1 & fig2 | fig3 & fig4)),
    )
    return marker

def run():
    env = os.getenv('FLASK_ENV')

    if (env == 'dev'):
        BASE_URL = "http://localhost:8000"
    else:
        BASE_URL = "https://api-v6-s6r4cnmwdq-ew.a.run.app"

    folium_map = folium.Map(location=[-36.6166642, -64.2833322], zoom_start=5)

    generar_marker('Capital Federal').add_to(folium_map)
    generar_marker('Buenos Aires').add_to(folium_map)
    generar_marker('Córdoba').add_to(folium_map)
    generar_marker('Catamarca').add_to(folium_map)
    generar_marker('Chaco').add_to(folium_map)
    generar_marker('Chubut').add_to(folium_map)
    generar_marker('Corrientes').add_to(folium_map)
    generar_marker('Entre Ríos').add_to(folium_map)
    generar_marker('Formosa').add_to(folium_map)
    generar_marker('Jujuy').add_to(folium_map)
    generar_marker('La Pampa').add_to(folium_map)
    generar_marker('La Rioja').add_to(folium_map)
    generar_marker('Mendoza').add_to(folium_map)
    generar_marker('Misiones').add_to(folium_map)
    generar_marker('Neuquén').add_to(folium_map)
    generar_marker('Río Negro').add_to(folium_map)
    generar_marker('Salta').add_to(folium_map)
    generar_marker('San Juan').add_to(folium_map)
    generar_marker('San Luis').add_to(folium_map)
    generar_marker('Santa Cruz').add_to(folium_map)
    generar_marker('Santa Fe').add_to(folium_map)
    generar_marker('Santiago del Estero').add_to(folium_map)
    generar_marker('Tierra del Fuego').add_to(folium_map)
    generar_marker('Tucumán').add_to(folium_map)

    region_json_df = gpd.read_file("datasets/provincia.json")

    region_json_df = region_json_df[['nam', 'geometry']]

    response = requests.get(f"{BASE_URL}/kpi_per_region")
    data = response.json()

    kpi_per_region_df = pd.read_json(data)

    kpi_per_region_df.fillna(0.0)

    region_match_per_region_df = region_json_df.merge(kpi_per_region_df,
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
    folium_geo_json = folium.features.GeoJson(
        data=region_match_per_region_df,
        style_function=style_function,
        control=False,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(
            fields=[
                'Provincia', 'Nro_de_centrales', 'Población_2020',
                'Consumo_total_por_población_provincia_GW'
            ],
            aliases=[
                'Provincia', 'Nro de centrales', 'Población 2020',
                'Consumo total por población provincia GW'
            ],
            style=
            ("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"
             )))



    folium_map.add_child(folium_geo_json)

    folium_static(folium_map, width=1738, height=1000)
