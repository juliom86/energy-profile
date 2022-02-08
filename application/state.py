import pandas as pd
import folium
import altair as alt

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
