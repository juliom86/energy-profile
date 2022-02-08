import pandas as pd
import geopandas as gpd
import folium
import requests
import os
from application import state
from streamlit_folium import folium_static

def run():
    env = os.getenv('FLASK_ENV')

    if (env == 'dev'):
        BASE_URL = "http://localhost:8000"
    else:
        BASE_URL = "https://api-v6-s6r4cnmwdq-ew.a.run.app"

    folium_map = folium.Map(location=[-36.6166642, -64.2833322], zoom_start=5)

    state.generar_marker('Capital Federal').add_to(folium_map)
    state.generar_marker('Buenos Aires').add_to(folium_map)
    state.generar_marker('Córdoba').add_to(folium_map)
    state.generar_marker('Catamarca').add_to(folium_map)
    state.generar_marker('Chaco').add_to(folium_map)
    state.generar_marker('Chubut').add_to(folium_map)
    state.generar_marker('Corrientes').add_to(folium_map)
    state.generar_marker('Entre Ríos').add_to(folium_map)
    state.generar_marker('Formosa').add_to(folium_map)
    state.generar_marker('Jujuy').add_to(folium_map)
    state.generar_marker('La Pampa').add_to(folium_map)
    state.generar_marker('La Rioja').add_to(folium_map)
    state.generar_marker('Mendoza').add_to(folium_map)
    state.generar_marker('Misiones').add_to(folium_map)
    state.generar_marker('Neuquén').add_to(folium_map)
    state.generar_marker('Río Negro').add_to(folium_map)
    state.generar_marker('Salta').add_to(folium_map)
    state.generar_marker('San Juan').add_to(folium_map)
    state.generar_marker('San Luis').add_to(folium_map)
    state.generar_marker('Santa Cruz').add_to(folium_map)
    state.generar_marker('Santa Fe').add_to(folium_map)
    state.generar_marker('Santiago del Estero').add_to(folium_map)
    state.generar_marker('Tierra del Fuego').add_to(folium_map)
    state.generar_marker('Tucumán').add_to(folium_map)

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
